"""
Local Email Department Classification Experiment.
Performs 5-department email routing across Jev Decision Model, Laya Encoder Model,
Llama 3.1 8B (Ollama), and Llama 3.2 1B (Ollama) on local hardware.

Evaluates Accuracy, Macro F1, Per-Department Precision/Recall, Latency (P50/P90/P99),
Throughput (emails/sec), and Expected Calibration Error (ECE).
"""

import sys
import os
import time
import json
import asyncio
import sqlite3
import numpy as np
import pandas as pd
from tabulate import tabulate

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.models import BenchmarkItem, DecisionOutput, AggregateMetric
from src.adapters import get_adapter
from src.metrics import calculate_ece


DEPARTMENTS = [
    "billing_finance",
    "technical_support",
    "sales_inquiries",
    "human_resources",
    "security_compliance"
]


def load_email_dataset() -> list[BenchmarkItem]:
    dataset_path = os.path.join(PROJECT_ROOT, "data", "email_department_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        raw_items = json.load(f)
        
    benchmark_items = []
    for item in raw_items:
        state_text = f"Subject: {item['subject']}\nBody: {item['body']}"
        benchmark_items.append(
            BenchmarkItem(
                id=item["id"],
                dataset_name="Email Department Classification",
                input_state={"email_content": state_text},
                question_key="target_department",
                question_instruction="Classify the incoming customer or enterprise email into exactly one of the 5 operational departments.",
                candidate_choices=DEPARTMENTS,
                ground_truth=item["ground_truth"]
            )
        )
    return benchmark_items


async def evaluate_model_on_emails(model_name: str, items: list[BenchmarkItem]) -> list[DecisionOutput]:
    adapter = get_adapter(model_name)
    outputs = []
    print(f"[*] Executing Email Classification for Model: {model_name} ({len(items)} emails)...")
    
    for i, item in enumerate(items):
        out = await adapter.predict_decision(item)
        outputs.append(out)
        if (i + 1) % 10 == 0 or (i + 1) == len(items):
            correct_cnt = sum(1 for o in outputs if o.is_correct)
            print(f"    -> [{model_name}] {i + 1}/{len(items)} completed | Running Accuracy: {correct_cnt}/{i + 1} ({correct_cnt / (i + 1) * 100:.1f}%)")
        
    return outputs


def compute_email_experiment_metrics(all_results: dict[str, list[DecisionOutput]]) -> dict[str, dict]:
    summary = {}
    
    for model_name, res_list in all_results.items():
        total = len(res_list)
        if total == 0:
            continue
            
        accuracies = [r.is_correct for r in res_list]
        confidences = [r.confidence_score for r in res_list]
        latencies = [r.latency_ms for r in res_list]
        
        acc = sum(accuracies) / total
        mean_lat = float(np.mean(latencies))
        p50_lat = float(np.percentile(latencies, 50))
        p90_lat = float(np.percentile(latencies, 90))
        p99_lat = float(np.percentile(latencies, 99))
        throughput = 1000.0 / mean_lat if mean_lat > 0 else 0.0
        ece = calculate_ece(confidences, accuracies)
        
        # Per-department Precision, Recall, F1
        dept_metrics = {}
        f1_list = []
        
        for dept in DEPARTMENTS:
            tp = sum(1 for r in res_list if r.chosen_label == dept and r.is_correct)
            fp = sum(1 for r in res_list if r.chosen_label == dept and not r.is_correct)
            fn = sum(1 for r in res_list if r.chosen_label != dept and not r.is_correct and hasattr(r, 'ground_truth') and r.ground_truth == dept)
            
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
            
            dept_metrics[dept] = {"precision": prec, "recall": rec, "f1": f1}
            f1_list.append(f1)
            
        macro_f1 = float(np.mean(f1_list))
        
        summary[model_name] = {
            "model_name": model_name,
            "total_emails": total,
            "accuracy": acc,
            "macro_f1": macro_f1,
            "mean_latency_ms": mean_lat,
            "p50_latency_ms": p50_lat,
            "p90_latency_ms": p90_lat,
            "p99_latency_ms": p99_lat,
            "throughput_emails_per_sec": throughput,
            "ece_calibration": ece,
            "dept_metrics": dept_metrics
        }
        
    return summary


def main():
    items = load_email_dataset()
    models_to_test = ["jev", "laya", "llama3.1:latest", "llama3.2:1b", "lukey03/qwen3.5-9b-abliterated"]
    
    print("\n========================================================")
    print("  LOCAL 5-DEPARTMENT EMAIL CLASSIFICATION EXPERIMENT")
    print(f"  Departments: {DEPARTMENTS}")
    print(f"  Total Emails: {len(items)}")
    print("========================================================\n")
    
    raw_output_path = os.path.join(PROJECT_ROOT, "data", "email_classification_results.json")
    existing_summary = {}
    if os.path.exists(raw_output_path):
        try:
            with open(raw_output_path, "r", encoding="utf-8") as f:
                existing_summary = json.load(f)
        except Exception:
            existing_summary = {}

    all_results = {}
    for model_name in models_to_test:
        if model_name in existing_summary and "--force" not in sys.argv and model_name != "lukey03/qwen3.5-9b-abliterated":
            print(f"[*] Using existing cached benchmark metrics for: {model_name}")
            continue
        results = asyncio.run(evaluate_model_on_emails(model_name, items))
        all_results[model_name] = results
        
    new_metrics = compute_email_experiment_metrics(all_results)
    existing_summary.update(new_metrics)
    metrics_summary = existing_summary
    
    # Save combined outputs to JSON
    with open(raw_output_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
        
    # Print formatted terminal summary table
    table_data = []
    for model_name, metric in metrics_summary.items():
        table_data.append([
            metric["model_name"],
            f"{metric['accuracy'] * 100:.1f}%",
            f"{metric['macro_f1'] * 100:.1f}%",
            f"{metric['p50_latency_ms']:.1f} ms",
            f"{metric['p99_latency_ms']:.1f} ms",
            f"{metric['throughput_emails_per_sec']:.2f} emails/s",
            f"{metric['ece_calibration']:.4f}"
        ])
        
    headers = ["Model Architecture", "Accuracy", "Macro F1", "P50 Latency", "P99 Latency", "Throughput", "ECE Calibration"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\n[+] Raw results saved to: {raw_output_path}")


if __name__ == "__main__":
    main()
