"""
Visualization script for generating publication-quality figures (300 DPI)
for the Jev vs. World & Jev vs. Laya Research Papers.
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
    
    colors = {'jev': '#1f77b4', 'laya': '#9467bd', 'gpt-4o-mini': '#ff7f0e', 'gpt-4o': '#2ca02c', 'llama3.1:latest': '#d62728', 'llama3.2:1b': '#8c564b'}
    
    for m in models:
        c = colors.get(m, '#7f7f7f')
        ax.scatter(costs[models.index(m)], accuracies[models.index(m)], s=160, color=c, label=summary[m].model_name, zorder=5, edgecolors='black')
        
        offset_y = 1.2 if m not in ['jev', 'laya'] else (-2.2 if m == 'jev' else 1.8)
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
    ax.set_ylim(40, 100)
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


def plot_jev_vs_laya_jevbench():
    """
    Plots JevBench v1.3.0 empirical benchmark scores comparing Jev 1.13.0 vs Laya open weights.
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    
    metrics = ["Composite Score", "Intelligence", "Calibration", "Standard Case Acc (%)", "Hard Case Acc (%)"]
    jev_scores = [74.4, 85.7, 82.7, 99.0, 74.1]
    laya_scores = [54.4, 45.8, 62.5, 72.9, 34.1]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, jev_scores, width, label='Jev 1.13.0 (Hosted API)', color='#1f77b4', edgecolor='black')
    rects2 = ax.bar(x + width/2, laya_scores, width, label='Laya (Open Weight Encoder)', color='#9467bd', edgecolor='black')
    
    ax.set_ylabel('Score / Percentage')
    ax.set_title('JevBench v1.3.0 Empirical Comparison: Jev vs. Laya')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold')
    ax.legend()
    ax.set_ylim(0, 110)
    ax.grid(axis='y', ls="--", alpha=0.5)
    
    # Annotate bars
    for bar in rects1:
        h = bar.get_height()
        ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=9)
    for bar in rects2:
        h = bar.get_height()
        ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig4_jev_vs_laya_scores.png"))
    plt.close()


def generate_all_plots():
    outputs = load_results_from_db()
    if outputs:
        summary = compute_aggregate_metrics(outputs)
        plot_cost_vs_accuracy(summary)
        plot_latency_cdf(outputs)
    plot_jev_vs_laya_jevbench()
    print(f"[+] Successfully generated figures in: {FIGURES_DIR}")


if __name__ == "__main__":
    generate_all_plots()
