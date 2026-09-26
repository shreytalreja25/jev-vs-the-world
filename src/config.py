"""
Configuration module for Jev vs. Frontier LLMs & Open-Weight Decision Models Benchmark Suite.
Defines model pricing, default parameters, dataset specifications, and execution modes.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ModelInfo:
    name: str
    provider: str  # 'typesafe', 'laya', 'openai', 'ollama', 'mock'
    model_id: str
    input_cost_per_1m: float   # USD per 1M input tokens
    output_cost_per_1m: float  # USD per 1M output tokens
    is_system_one: bool = False
    max_context_tokens: int = 4096
    notes: str = ""


# Model pricing & registry
MODEL_REGISTRY: Dict[str, ModelInfo] = {
    "jev": ModelInfo(
        name="Jev (TypeSafe AI)",
        provider="typesafe",
        model_id="jev-v1",
        input_cost_per_1m=0.042,
        output_cost_per_1m=0.0,  # Jev output tokens are free / zero generation cost
        is_system_one=True,
        max_context_tokens=65536,  # 64k token context window
        notes="Managed System-One decision API. 64k context, zero output token overhead.",
    ),
    "laya": ModelInfo(
        name="Laya (Open-Weight Encoder)",
        provider="laya",
        model_id="laya-v1-open",
        input_cost_per_1m=0.00,  # Self-hosted open-weights Apache-2.0
        output_cost_per_1m=0.00,
        is_system_one=True,
        max_context_tokens=512,  # 512 token context window per question
        notes="Open-weight encoder decision model (Apache-2.0). 512-token context window.",
    ),
    "gpt-4o-mini": ModelInfo(
        name="GPT-4o Mini",
        provider="openai",
        model_id="gpt-4o-mini",
        input_cost_per_1m=0.15,
        output_cost_per_1m=0.60,
        is_system_one=False,
        max_context_tokens=128000,
        notes="Lightweight general LLM with JSON mode.",
    ),
    "gpt-4o": ModelInfo(
        name="GPT-4o",
        provider="openai",
        model_id="gpt-4o",
        input_cost_per_1m=2.50,
        output_cost_per_1m=10.00,
        is_system_one=False,
        max_context_tokens=128000,
        notes="Frontier general LLM with JSON mode.",
    ),
    "llama3.1:latest": ModelInfo(
        name="Llama 3.1 8B (Local Ollama)",
        provider="ollama",
        model_id="llama3.1:latest",
        input_cost_per_1m=0.00,
        output_cost_per_1m=0.00,
        is_system_one=False,
        max_context_tokens=128000,
        notes="Open-source local 8B LLM running via Ollama.",
    ),
    "llama3.2:1b": ModelInfo(
        name="Llama 3.2 1B (Local Ollama)",
        provider="ollama",
        model_id="llama3.2:1b",
        input_cost_per_1m=0.00,
        output_cost_per_1m=0.00,
        is_system_one=False,
        max_context_tokens=128000,
        notes="Ultra-compact open-source 1B LLM running via Ollama.",
    ),
    "mock-fast": ModelInfo(
        name="Mock Fast System-One",
        provider="mock",
        model_id="mock-fast",
        input_cost_per_1m=0.042,
        output_cost_per_1m=0.0,
        is_system_one=True,
        max_context_tokens=65536,
        notes="Mock adapter simulating sub-100ms decision latency.",
    )
}

# General paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RESULTS_DB_PATH = os.path.join(PROJECT_ROOT, "data", "benchmark_results.db")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "analysis", "figures")
PAPER_DIR = os.path.join(PROJECT_ROOT, "paper")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(PAPER_DIR, exist_ok=True)
