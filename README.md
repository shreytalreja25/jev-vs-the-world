# Jev vs. The World: Tokenomics, Performance & Open-Weight Encoder Benchmark Suite

[![Main Paper PDF](https://img.shields.io/badge/Main_Paper-PDF-red)](paper/research_paper.pdf)
[![Jev vs Laya Paper PDF](https://img.shields.io/badge/Jev_vs_Laya_Paper-PDF-purple)](paper/jev_vs_laya.pdf)
[![Email Experiment PDF](https://img.shields.io/badge/Email_Experiment-PDF-green)](paper/email_classification_report.pdf)
[![GitHub Repository](https://img.shields.io/badge/GitHub-shreytalreja25%2Fjev--vs--the--world-black)](https://github.com/shreytalreja25/jev-vs-the-world.git)

An empirical benchmark suite and triple research paper collection comparing **Jev (TypeSafe AI's System-One model)** against open-weight decision encoders (**Laya**), local open-source models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama), and frontier LLMs (**GPT-4o**, **GPT-4o-mini**).

---

## 📚 Triple Research Paper Collection (IEEE Formatting)

1. 📖 **Main Research Paper ([paper/research_paper.pdf](paper/research_paper.pdf) | [Markdown](paper/research_paper.md))**:
   * *Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs and Open-Weight Encoders*
2. 📄 **Dedicated Jev vs. Laya Paper ([paper/jev_vs_laya.pdf](paper/jev_vs_laya.pdf) | [Markdown](paper/jev_vs_laya_paper.md))**:
   * *Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures*
3. ✉️ **Local Email Classification Experiment Paper ([paper/email_classification_report.pdf](paper/email_classification_report.pdf) | [Markdown](paper/email_classification_report.md))**:
   * *Empirical Evaluation of Local Open-Source LLMs and Decision Models in Enterprise 5-Department Email Routing*

---

## ✉️ Local 5-Department Email Routing Experiment

Evaluated on a 50-item enterprise email dataset categorized across 5 departments (`billing_finance`, `technical_support`, `sales_inquiries`, `human_resources`, `security_compliance`) running locally on a developer laptop:

| Model Architecture | Source / Provider | Accuracy (%) | Macro F1 (%) | P50 Latency (ms) | Throughput (Emails/sec) | ECE Calibration |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Llama 3.1 8B** | Local Ollama | **96.0%** | **96.0%** | 1,410.0 ms | 0.71 emails/s | **0.0410** |
| **Jev (TypeSafe AI)** | System-One API | **90.0%** | **89.8%** | **97.0 ms** | **10.31 emails/s** | **0.0210** |
| **Laya** | Open-Weight Encoder | 78.0% | 77.2% | **58.0 ms** | **17.24 emails/s** | 0.1240 |
| **Llama 3.2 1B** | Local Ollama | 52.0% | 49.5% | 1,020.0 ms | 0.98 emails/s | 0.3850 |

### Key Analytical Conclusions:
* **Accuracy Champion**: **Llama 3.1 8B** achieves **96.0% accuracy**, demonstrating superior multi-class domain reasoning across enterprise email subjects and body contents.
* **Throughput & Speed Champion**: **Laya** (**17.24 emails/sec**) and **Jev** (**10.31 emails/sec**) process incoming emails **14x to 24x faster** than generative LLMs with sub-100ms P50 latency.

---

## 🛠️ Execution & Reproduction

```bash
# Run local 5-department email classification experiment
python experiments/email_department_classification.py

# Generate experiment visual figures
python analysis/visualize_email_exp.py

# Recompile IEEE PDF report
python paper/generate_email_pdf.py
```

---

## 📜 Citations

```bibtex
@article{talreja2026email_exp,
  title={Empirical Evaluation of Local Open-Source LLMs and Decision Models in Enterprise 5-Department Email Routing},
  author={Talreja, Shrey and Antigravity AI},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}
```
