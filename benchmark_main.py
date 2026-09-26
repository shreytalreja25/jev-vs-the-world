"""
Main entry point for running the Jev vs. Frontier LLMs & Open Source benchmark.
"""

import asyncio
import argparse
import sys
from src.datasets.benchmark_datasets import load_all_datasets
from src.runner import run_full_suite


def main():
    parser = argparse.ArgumentParser(description="Jev vs. Frontier & Open Source LLMs Tokenomics Benchmark")
    parser.add_argument("--models", nargs="+", default=["jev", "gpt-4o-mini", "gpt-4o", "llama3.1:latest", "llama3.2:1b"],
                        help="List of model keys from MODEL_REGISTRY to benchmark")
    args = parser.parse_args()

    items = load_all_datasets()
    asyncio.run(run_full_suite(args.models, items))


if __name__ == "__main__":
    main()
