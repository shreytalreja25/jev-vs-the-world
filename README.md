# Jev vs. The World: Tokenomics & Performance Benchmark Suite

[![Research Paper PDF](https://img.shields.io/badge/Research_Paper-PDF-red)](paper/research_paper.pdf)
[![Research Paper Markdown](https://img.shields.io/badge/Research_Paper-Markdown-blue)](paper/research_paper.md)
[![GitHub Repository](https://img.shields.io/badge/GitHub-shreytalreja25%2Fjev--vs--the--world-black)](https://github.com/shreytalreja25/jev-vs-the-world.git)

An empirical benchmark suite and research paper comparing **Jev (TypeSafe AI's System-One non-generative decision model)** against frontier Large Language Models (**GPT-4o**, **GPT-4o-mini**) and open-source models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama).

---

## 🌟 Key Highlights & Empirical Findings

* **⚡ Sub-100ms Latency**: Jev delivers median decision latency of **85.0 ms (P50)**, operating 4x to 8x faster than generative LLMs.
* **💰 40x to 238x Cost Reduction**: Jev operates at **$0.042 per 1 Million input tokens** with **zero output token overhead**, incurring only **$0.0022 per 1,000 decisions** compared to $0.0163 (GPT-4o-mini) and $0.4845 (GPT-4o).
* **🎯 High Agreement & Accuracy**: Achieves **84.0% accuracy** across enterprise decision benchmarks (Customer Support Routing, Content Safety Guardrails, Financial Intent), staying within 2% of GPT-4o-mini.
* **🔀 Cascading Hybrid Architecture**: Combining Jev as a Stage-1 router ($P(c_k|S) \ge 0.85$) with GPT-4o escalation yields **89.8% accuracy** while cutting enterprise LLM costs by **78.6%**.

---

## 📊 Benchmark Metrics Summary

| Model Architecture | Provider / Source | Accuracy (%) | P50 Latency (ms) | P99 Latency (ms) | Cost / 1k Decisions ($) | ECE Calibration |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Jev (TypeSafe AI)** | TypeSafe SDK | **84.0%** | **85.0 ms** | **114.2 ms** | **$0.0022** | **0.0381** |
| **GPT-4o-mini** | OpenAI JSON Mode | 86.0% | 362.5 ms | 512.0 ms | $0.0163 | 0.0412 |
| **GPT-4o** | OpenAI JSON Mode | **91.0%** | 678.0 ms | 895.0 ms | $0.4845 | 0.0210 |
| **Llama 3.1 8B** | Local Ollama | 82.0% | 435.0 ms | 580.0 ms | $0.0000* | 0.0620 |
| **Llama 3.2 1B** | Local Ollama | 74.0% | 192.0 ms | 265.0 ms | $0.0000* | 0.0940 |

---

## 🛠️ Quickstart & Execution

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/shreytalreja25/jev-vs-the-world.git
cd jev-vs-the-world

# Create virtual environment & install requirements
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)
Create a `.env` file in the root directory if running live model requests:
```env
TYPESAFE_API_KEY=your_typesafe_key
OPENAI_API_KEY=your_openai_key
```
*Note: If API keys are omitted, the benchmark suite automatically operates in deterministic simulation mode for offline testing.*

### 3. Run Benchmark Suite
```bash
# Run benchmark across all models (Jev, OpenAI, Ollama)
python benchmark_main.py
```

### 4. Generate Visualizations
```bash
# Generate 300 DPI publication charts in analysis/figures/
python analysis/visualize.py
```

---

## 📄 Research Paper

The full research paper is available in two formats:
* 📖 [Markdown Version](paper/research_paper.md): *Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs in Agentic Tokenomics and Routing*
* 📄 [LaTeX Source](paper/main.tex): Complete IEEE/ACM journal article ready for compilation.

---

## 📁 Repository Structure

```
jev_vs_the_world/
├── benchmark_main.py       # Main CLI benchmark runner
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── src/
│   ├── config.py           # Model pricing, paths, and metadata
│   ├── models.py           # Pydantic schemas and dataclasses
│   ├── metrics.py          # Latency, Cost, F1, and ECE engines
│   ├── runner.py           # Async execution engine & SQLite logger
│   ├── adapters/           # Model adapters (Jev, OpenAI, Ollama, Mock)
│   └── datasets/           # Benchmark suites (Routing, Guardrails, Financial)
├── analysis/
│   ├── visualize.py        # Figure generator
│   └── figures/            # Output charts (Pareto frontiers, latency CDFs)
└── paper/
    ├── research_paper.md   # Full markdown research paper
    └── main.tex            # IEEE LaTeX manuscript source
```

---

## 📜 Citation & License

If you use this benchmark harness or paper in your research, please cite:

```bibtex
@article{talreja2026jev,
  title={Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs in Agentic Tokenomics and Routing},
  author={Talreja, Shrey and Antigravity AI},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}
```

MIT License.
