"""
Visualization script for Local Multi-Step Agentic Pipeline Experiment.
Generates publication-grade figures in analysis/figures/.
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


def generate_agentic_plots():
    results_path = os.path.join(PROJECT_ROOT, "data", "agentic_pipeline_results.json")
    if not os.path.exists(results_path):
        print(f"[!] Agentic pipeline results file not found at: {results_path}")
        return
        
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    configs = list(data.keys())
    s1_lats = [data[c]["mean_stage1_lat_ms"] for c in configs]
    s2_lats = [data[c]["mean_stage2_lat_ms"] for c in configs]
    s3_lats = [data[c]["mean_stage3_lat_ms"] for c in configs]
    s4_lats = [data[c]["mean_stage4_lat_ms"] for c in configs]
    
    triage_accs = [data[c]["triage_accuracy"] * 100.0 for c in configs]
    verify_rates = [data[c]["verification_pass_rate"] * 100.0 for c in configs]

    # 1. Fig 7: Per-Stage Latency Breakdown
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    x = np.arange(len(configs))
    width = 0.45
    
    p1 = ax.bar(x, s1_lats, width, label='Stage 1: Triage Router', color='#1f77b4', edgecolor='black')
    p2 = ax.bar(x, s2_lats, width, bottom=s1_lats, label='Stage 2: Threat Analysis', color='#ff7f0e', edgecolor='black')
    p3 = ax.bar(x, s3_lats, width, bottom=np.array(s1_lats)+np.array(s2_lats), label='Stage 3: Patch Generation', color='#2ca02c', edgecolor='black')
    p4 = ax.bar(x, s4_lats, width, bottom=np.array(s1_lats)+np.array(s2_lats)+np.array(s3_lats), label='Stage 4: Policy Verification', color='#d62728', edgecolor='black')
    
    ax.set_ylabel('Execution Latency (ms)')
    ax.set_title('Per-Stage Latency Breakdown in 4-Stage Agentic Pipeline')
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontweight='bold', rotation=10)
    ax.legend(loc='upper left')
    ax.grid(axis='y', ls="--", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig7_agentic_pipeline_latency_breakdown.png"))
    plt.close()

    # 2. Fig 8: Triage Accuracy vs Verification Pass Rate
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    width_b = 0.35
    
    r1 = ax.bar(x - width_b/2, triage_accs, width_b, label='Stage 1 Triage Accuracy (%)', color='#1f77b4', edgecolor='black')
    r2 = ax.bar(x + width_b/2, verify_rates, width_b, label='Stage 4 Policy Pass Rate (%)', color='#2ca02c', edgecolor='black')
    
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Agentic Pipeline Accuracy vs. Policy Verification Pass Rate')
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontweight='bold', rotation=10)
    ax.legend()
    ax.set_ylim(0, 110)
    ax.grid(axis='y', ls="--", alpha=0.5)
    
    for bar in r1:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=9)
    for bar in r2:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig8_agentic_remediation_success.png"))
    plt.close()

    print(f"[+] Successfully generated Agentic Pipeline figures in: {FIGURES_DIR}")


if __name__ == "__main__":
    generate_agentic_plots()
