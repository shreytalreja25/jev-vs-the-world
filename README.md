# Jev vs. The World: Tokenomics, Performance & Open-Weight Encoder Benchmark Suite

[![Main Paper PDF](https://img.shields.io/badge/Main_Paper-PDF-red)](paper/research_paper.pdf)
[![Jev vs Laya Paper PDF](https://img.shields.io/badge/Jev_vs_Laya_Paper-PDF-purple)](paper/jev_vs_laya.pdf)
[![GitHub Repository](https://img.shields.io/badge/GitHub-shreytalreja25%2Fjev--vs--the--world-black)](https://github.com/shreytalreja25/jev-vs-the-world.git)

An empirical benchmark suite and dual research paper collection comparing **Jev (TypeSafe AI's System-One model)** against open-weight decision encoders (**Laya**), frontier Large Language Models (**GPT-4o**, **GPT-4o-mini**), and open-source local models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama).

---

## 📚 Dual Research Paper Collection

1. 📖 **Main Research Paper ([paper/research_paper.pdf](paper/research_paper.pdf) | [Markdown](paper/research_paper.md))**:
   * *Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs and Open-Weight Encoders in Agentic Tokenomics*
2. 📄 **Dedicated Second Paper ([paper/jev_vs_laya.pdf](paper/jev_vs_laya.pdf) | [Markdown](paper/jev_vs_laya_paper.md))**:
   * *Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures*
   * *Citing Hugging Face Community Guide (September 24, 2026)*

---

## 📊 Jev vs. Laya: Operating Boundary Comparison

| Dimension / Metric | Jev (TypeSafe AI) | Laya (Open-Weight Encoder) | Operational Implication |
| :--- | :--- | :--- | :--- |
| **Deployment Model** | Managed Cloud API | Open Weights (Apache-2.0) | Laya enables 100% on-premise air-gapped data residency. |
| **Composite Benchmark Score** | **74.4 (#1)** | 54.4 (#33) | Jev delivers superior overall decision performance out of the box. |
| **Hard-Case Accuracy** | **74.1%** | 34.1% | Jev excels at ambiguous and multi-step policy logic. |
| **Standard-Case Accuracy** | **99.0%** | 72.9% | Laya requires task fine-tuning for domain stability. |
| **Context Window Limit** | **64,000 tokens** | 512 tokens / question | Jev processes long tickets/logs without truncation errors. |
| **Calibration Score (ECE)** | **82.7 (ECE = 0.0206)** | 62.5 (ECE = 0.1240) | Jev confidence probabilities enable immediate cascading routing. |
| **GPU Operations Burden** | Zero GPU management | GPU hosting required | Jev requires zero infrastructure ops or monitoring overhead. |

---

## 🛠️ Benchmark Execution

```bash
# Clone the repository
git clone https://github.com/shreytalreja25/jev-vs-the-world.git
cd jev-vs-the-world

# Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# Run benchmark suite across Jev, Laya, OpenAI, and Ollama
python benchmark_main.py

# Generate publication-grade 300 DPI figures
python analysis/visualize.py

# Recompile PDF papers
python paper/generate_pdf.py
python paper/generate_laya_pdf.py
```

---

## 📜 Citations

```bibtex
@article{talreja2026jev,
  title={Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs and Open-Weight Encoders},
  author={Talreja, Shrey and Antigravity AI},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}

@article{talreja2026jev_laya,
  title={Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures},
  author={Talreja, Shrey and Antigravity AI},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}
```
