"""
Main entry point for running the Jev vs. Laya & Frontier/Open-Source LLMs Benchmark.
"""

import asyncio
import argparse
import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.datasets.benchmark_datasets import load_all_datasets
from src.runner import run_full_suite


def main():
    parser = argparse.ArgumentParser(description="Jev vs. Laya & Frontier/Open-Source LLMs Tokenomics Benchmark")
    parser.add_argument("--models", nargs="+", default=["jev", "laya", "gpt-4o-mini", "gpt-4o", "llama3.1:latest", "llama3.2:1b"],
                        help="List of model keys from MODEL_REGISTRY to benchmark")
    args = parser.parse_args()

    items = load_all_datasets()
    asyncio.run(run_full_suite(args.models, items))


if __name__ == "__main__":
    main()
