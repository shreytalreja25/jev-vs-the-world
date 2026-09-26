"""
Benchmark runner executing decision evaluation across models, datasets, and adapters.
Saves results into SQLite database for reproducibility.
"""

import asyncio
import sqlite3
import json
import time
from typing import List, Dict
from tabulate import tabulate

from src.config import RESULTS_DB_PATH
from src.models import BenchmarkItem, DecisionOutput, AggregateMetric
from src.adapters import get_adapter
from src.metrics import compute_aggregate_metrics


def init_db(db_path: str = RESULTS_DB_PATH):
    """
    Initializes SQLite table for persistent decision logging.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        item_id TEXT,
        dataset_name TEXT,
        model_name TEXT,
        chosen_label TEXT,
        confidence_score REAL,
        is_correct INTEGER,
        latency_ms REAL,
        input_tokens INTEGER,
        output_tokens INTEGER,
        estimated_cost_usd REAL,
        raw_response TEXT
    )
    """)
    conn.commit()
    conn.close()


def save_results_to_db(results: List[DecisionOutput], db_path: str = RESULTS_DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for r in results:
        cursor.execute("""
        INSERT INTO benchmark_runs 
        (item_id, dataset_name, model_name, chosen_label, confidence_score, is_correct, latency_ms, input_tokens, output_tokens, estimated_cost_usd, raw_response)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.item_id, r.dataset_name, r.model_name, r.chosen_label, r.confidence_score,
            1 if r.is_correct else 0, r.latency_ms, r.input_tokens, r.output_tokens,
            r.estimated_cost_usd, r.raw_response
        ))
    conn.commit()
    conn.close()


async def run_benchmark_for_model(model_name: str, items: List[BenchmarkItem]) -> List[DecisionOutput]:
    adapter = get_adapter(model_name)
    outputs = []
    for item in items:
        out = await adapter.predict_decision(item)
        outputs.append(out)
    return outputs


async def run_full_suite(models: List[str], items: List[BenchmarkItem]) -> Dict[str, AggregateMetric]:
    init_db()
    all_outputs = []
    
    print(f"\n========================================================")
    print(f"   STARTING JEV vs THE WORLD BENCHMARK SUITE")
    print(f"   Models: {models}")
    print(f"   Total Test Items: {len(items)}")
    print(f"========================================================\n")
    
    for model_name in models:
        print(f"[*] Running benchmark for: {model_name}...")
        outputs = await run_benchmark_for_model(model_name, items)
        all_outputs.extend(outputs)
        print(f"    Completed {len(outputs)} samples.")
        
    save_results_to_db(all_outputs)
    summary = compute_aggregate_metrics(all_outputs)
    
    # Print formatted terminal summary table
    table_data = []
    for model_name, metric in summary.items():
        table_data.append([
            metric.model_name,
            f"{metric.accuracy * 100:.1f}%",
            f"{metric.p50_latency_ms:.1f} ms",
            f"{metric.p99_latency_ms:.1f} ms",
            f"${metric.cost_per_1k_decisions:.4f}",
            f"{metric.expected_calibration_error:.4f}",
            metric.total_input_tokens,
            metric.total_output_tokens
        ])
        
    headers = ["Model", "Accuracy", "P50 Latency", "P99 Latency", "Cost/1k Decisions", "ECE Calibration", "In Tokens", "Out Tokens"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    return summary
