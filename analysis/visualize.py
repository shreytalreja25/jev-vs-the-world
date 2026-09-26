"""
Visualization script for generating publication-quality figures (300 DPI)
for the Jev vs. Frontier LLMs Research Paper.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import RESULTS_DB_PATH, FIGURES_DIR
from src.metrics import compute_aggregate_metrics
from src.models import DecisionOutput


# Set publication style settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'figure.dpi': 300
})


def load_results_from_db(db_path: str = RESULTS_DB_PATH) -> list[DecisionOutput]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT item_id, dataset_name, model_name, chosen_label, confidence_score, is_correct, latency_ms, input_tokens, output_tokens, estimated_cost_usd, raw_response
    FROM benchmark_runs
    """)
    rows = cursor.fetchall()
    conn.close()
    
    outputs = []
    for r in rows:
        outputs.append(DecisionOutput(
            item_id=r[0],
            dataset_name=r[1],
            model_name=r[2],
            chosen_label=r[3],
            confidence_score=r[4],
            is_correct=bool(r[5]),
            latency_ms=r[6],
            input_tokens=r[7],
            output_tokens=r[8],
            estimated_cost_usd=r[9],
            raw_response=r[10]
        ))
    return outputs


def plot_cost_vs_accuracy(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    models = list(summary.keys())
    accuracies = [summary[m].accuracy * 100.0 for m in models]
    costs = [summary[m].cost_per_1k_decisions for m in models]
    
    # Custom colors & markers
    colors = {'jev': '#1f77b4', 'gpt-4o-mini': '#ff7f0e', 'gpt-4o': '#2ca02c', 'llama3.1:latest': '#d62728', 'llama3.2:1b': '#9467bd'}
    
    for m in models:
        c = colors.get(m, '#7f7f7f')
        ax.scatter(costs[models.index(m)], accuracies[models.index(m)], s=160, color=c, label=summary[m].model_name, zorder=5, edgecolors='black')
        
        # Annotation text offset
        offset_y = 1.2 if m != 'jev' else -2.2
        offset_x = 0.005 if summary[m].cost_per_1k_decisions > 0.01 else 0.001
        ax.annotate(
            summary[m].model_name,
            (summary[m].cost_per_1k_decisions + offset_x, summary[m].accuracy * 100.0 + offset_y),
            fontsize=9.5, fontweight='bold'
        )
        
    ax.set_xscale('log')
    ax.set_xlabel("Cost per 1,000 Decisions ($ USD, Log Scale)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Pareto Efficiency: Cost vs. Accuracy Across Decision Architectures")
    ax.set_ylim(60, 100)
    ax.grid(True, which="both", ls="--", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig1_cost_vs_accuracy_pareto.png"))
    plt.close()


def plot_latency_cdf(outputs):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    df = pd.DataFrame([{
        'model_name': o.model_name,
        'latency_ms': o.latency_ms
    } for o in outputs])
    
    for model_name, group in df.groupby('model_name'):
        sorted_lat = np.sort(group['latency_ms'])
        cdf = np.arange(1, len(sorted_lat) + 1) / len(sorted_lat)
        ax.plot(sorted_lat, cdf * 100, label=model_name, linewidth=2.2)
        
    ax.axvline(x=100, color='red', linestyle=':', label='Sub-100ms SLA Target')
    ax.set_xscale('log')
    ax.set_xlabel("Latency (ms, Log Scale)")
    ax.set_ylabel("Cumulative Percentile (%)")
    ax.set_title("Latency Cumulative Distribution Function (CDF)")
    ax.legend(loc="lower right")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig2_latency_cdf.png"))
    plt.close()


def plot_cost_savings_per_million(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    models = list(summary.keys())
    costs_per_million = [summary[m].cost_per_1k_decisions * 1000.0 for m in models]
    labels = [summary[m].model_name for m in models]
    
    bars = ax.bar(labels, costs_per_million, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'], edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=9.5)
                    
    ax.set_ylabel("Total Cost per 1 Million Decisions ($ USD)")
    ax.set_title("Enterprise Scale Cost Comparison: 1 Million System-One Invocations")
    ax.set_yscale('log')
    ax.grid(axis='y', ls="--", alpha=0.5)
    plt.xticks(rotation=15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig3_cost_savings_bar.png"))
    plt.close()


def generate_all_plots():
    outputs = load_results_from_db()
    if not outputs:
        print("[!] No benchmark outputs found in DB to plot.")
        return
        
    summary = compute_aggregate_metrics(outputs)
    plot_cost_vs_accuracy(summary)
    plot_latency_cdf(outputs)
    plot_cost_savings_per_million(summary)
    print(f"[+] Successfully generated figures in: {FIGURES_DIR}")


if __name__ == "__main__":
    generate_all_plots()
