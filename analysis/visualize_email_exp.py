"""
Visualization script for Local Email Department Classification Experiment.
Generates 3 dedicated publication-grade charts in analysis/figures/.
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.config import FIGURES_DIR


plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'figure.dpi': 300
})


def generate_email_plots():
    results_path = os.path.join(PROJECT_ROOT, "data", "email_classification_results.json")
    if not os.path.exists(results_path):
        print(f"[!] Email experiment results file not found at: {results_path}")
        return
        
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    models = list(data.keys())
    model_name_map = {
        "jev": "Jev",
        "laya": "Laya",
        "llama3.1:latest": "Llama 3.1 8B",
        "llama3.2:1b": "Llama 3.2 1B",
        "lukey03/qwen3.5-9b-abliterated": "Qwen 3.5 9B"
    }
    display_names = [model_name_map.get(m, m) for m in models]
    
    accuracies = [data[m]["accuracy"] * 100.0 for m in models]
    macro_f1s = [data[m]["macro_f1"] * 100.0 for m in models]
    p50_lats = [data[m]["p50_latency_ms"] for m in models]
    throughputs = [data[m]["throughput_emails_per_sec"] for m in models]
    
    # 1. Fig 5: Email Accuracy & Macro F1
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    x = np.arange(len(models))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, accuracies, width, label='Accuracy (%)', color='#1f77b4', edgecolor='black')
    rects2 = ax.bar(x + width/2, macro_f1s, width, label='Macro F1 (%)', color='#ff7f0e', edgecolor='black')
    
    ax.set_ylabel('Percentage (%)')
    ax.set_title('5-Department Email Classification Performance')
    ax.set_xticks(x)
    ax.set_xticklabels(display_names, fontweight='bold')
    ax.legend()
    ax.set_ylim(0, 115)
    ax.grid(axis='y', ls="--", alpha=0.5)
    
    for bar in rects1:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=8.5)
    for bar in rects2:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig5_email_accuracy_f1.png"))
    plt.close()

    # 2. Fig 6: Latency P50 vs Throughput
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    color = '#2ca02c'
    ax1.set_xlabel('Model Architecture', fontweight='bold')
    ax1.set_ylabel('P50 Latency (ms)', color=color, fontweight='bold')
    bars1 = ax1.bar(x - width/2, p50_lats, width, color=color, alpha=0.8, edgecolor='black', label='P50 Latency (ms)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = '#d62728'
    ax2.set_ylabel('Throughput (Emails / sec)', color=color, fontweight='bold')
    bars2 = ax2.bar(x + width/2, throughputs, width, color=color, alpha=0.8, edgecolor='black', label='Throughput (emails/s)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(display_names, fontweight='bold')
    plt.title('Email Classification Latency (P50) vs. Processing Throughput')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig6_email_latency_throughput.png"))
    plt.close()

    print(f"[+] Successfully generated Email Experiment figures in: {FIGURES_DIR}")


if __name__ == "__main__":
    generate_email_plots()
