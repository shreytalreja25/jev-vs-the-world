"""
Metrics calculation module for evaluating model performance, latency, tokenomics cost, and calibration error.
"""

import numpy as np
from typing import List, Dict, Any
from src.models import DecisionOutput, AggregateMetric


def calculate_ece(confidences: List[float], accuracies: List[bool], n_bins: int = 10) -> float:
    """
    Calculates Expected Calibration Error (ECE) across confidence probability bins.
    """
    if not confidences or len(confidences) == 0:
        return 0.0
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    total_samples = len(confidences)
    
    conf_arr = np.array(confidences)
    acc_arr = np.array(accuracies, dtype=float)
    
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        in_bin = (conf_arr > bin_lower) & (conf_arr <= bin_upper)
        bin_size = np.sum(in_bin)
        
        if bin_size > 0:
            bin_acc = np.mean(acc_arr[in_bin])
            bin_conf = np.mean(conf_arr[in_bin])
            ece += (bin_size / total_samples) * np.abs(bin_acc - bin_conf)
            
    return float(ece)


def compute_aggregate_metrics(results: List[DecisionOutput]) -> Dict[str, AggregateMetric]:
    """
    Groups decision outputs by model_name and computes summary performance & tokenomic metrics.
    """
    by_model: Dict[str, List[DecisionOutput]] = {}
    for res in results:
        by_model.setdefault(res.model_name, []).append(res)
        
    metrics_summary: Dict[str, AggregateMetric] = {}
    
    for model_name, res_list in by_model.items():
        total = len(res_list)
        if total == 0:
            continue
            
        accuracies = [r.is_correct for r in res_list]
        confidences = [r.confidence_score for r in res_list]
        latencies = [r.latency_ms for r in res_list]
        costs = [r.estimated_cost_usd for r in res_list]
        in_tokens = [r.input_tokens for r in res_list]
        out_tokens = [r.output_tokens for r in res_list]
        
        accuracy = sum(accuracies) / total
        mean_lat = float(np.mean(latencies))
        p50_lat = float(np.percentile(latencies, 50))
        p90_lat = float(np.percentile(latencies, 90))
        p99_lat = float(np.percentile(latencies, 99))
        
        tot_cost = sum(costs)
        cost_per_1k = (tot_cost / total) * 1000.0 if total > 0 else 0.0
        ece = calculate_ece(confidences, accuracies)
        
        # Calculate Macro F1
        truth_labels = [r.ground_truth if hasattr(r, 'ground_truth') else r.chosen_label for r in res_list]
        unique_classes = set(r.chosen_label for r in res_list)
        f1_scores = []
        for cls in unique_classes:
            tp = sum(1 for r in res_list if r.chosen_label == cls and r.is_correct)
            fp = sum(1 for r in res_list if r.chosen_label == cls and not r.is_correct)
            fn = sum(1 for r in res_list if r.chosen_label != cls and not r.is_correct)
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
            f1_scores.append(f1)
        macro_f1 = float(np.mean(f1_scores)) if f1_scores else accuracy
        
        metrics_summary[model_name] = AggregateMetric(
            model_name=model_name,
            total_samples=total,
            accuracy=accuracy,
            macro_f1=macro_f1,
            mean_latency_ms=mean_lat,
            p50_latency_ms=p50_lat,
            p90_latency_ms=p90_lat,
            p99_latency_ms=p99_lat,
            total_cost_usd=tot_cost,
            cost_per_1k_decisions=cost_per_1k,
            expected_calibration_error=ece,
            total_input_tokens=sum(in_tokens),
            total_output_tokens=sum(out_tokens)
        )
        
    return metrics_summary
