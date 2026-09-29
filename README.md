# Jev vs. The World: Tokenomics, Performance & Open-Weight Encoder Benchmark Suite

[![Main Paper PDF](https://img.shields.io/badge/Main_Paper-PDF-red)](paper/research_paper.pdf)
[![Jev vs Laya Paper PDF](https://img.shields.io/badge/Jev_vs_Laya_Paper-PDF-purple)](paper/jev_vs_laya.pdf)
[![Email Experiment PDF](https://img.shields.io/badge/Email_Experiment-PDF-green)](paper/email_classification_report.pdf)
[![Agentic Pipeline PDF](https://img.shields.io/badge/Agentic_Pipeline-PDF-orange)](paper/agentic_pipeline_report.pdf)
[![GitHub Repository](https://img.shields.io/badge/GitHub-shreytalreja25%2Fjev--vs--the--world-black)](https://github.com/shreytalreja25/jev-vs-the-world.git)

An empirical benchmark suite and quad research paper collection comparing **Jev (TypeSafe AI's System-One model)** against open-weight decision encoders (**Laya**), local open-source models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama), and frontier LLMs (**GPT-4o**, **GPT-4o-mini**).

---

## 📚 Quad Research Paper Collection (Official IEEE 2-Column Formatting)

1. 📖 **Main Research Paper ([paper/research_paper.pdf](paper/research_paper.pdf) | [Markdown](paper/research_paper.md))**:
   * *Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs and Open-Weight Encoders*
2. 📄 **Dedicated Jev vs. Laya Paper ([paper/jev_vs_laya.pdf](paper/jev_vs_laya.pdf) | [Markdown](paper/jev_vs_laya_paper.md))**:
   * *Hosted API vs. Open-Weight Encoder Models: An Empirical Evaluation of Jev and Laya in Enterprise Decision Architectures*
3. ✉️ **Local Email Classification Paper ([paper/email_classification_report.pdf](paper/email_classification_report.pdf) | [Markdown](paper/email_classification_report.md))**:
   * *Empirical Evaluation of Local Open-Source LLMs and Decision Models in Enterprise 5-Department Email Routing*
4. 🛡️ **Local Agentic Pipeline Paper ([paper/agentic_pipeline_report.pdf](paper/agentic_pipeline_report.pdf) | [Markdown](paper/agentic_pipeline_report.md))**:
   * *Autonomous Code Vulnerability Triage, Threat Analysis, and Patch Remediation via Local Multi-Stage Agentic Pipelines*

---

## 🛠️ Execution & Reproduction

```bash
# Run local 5-department email classification experiment
python experiments/email_department_classification.py

# Run local 4-stage agentic security pipeline
python experiments/agentic_vulnerability_pipeline.py

# Recompile IEEE PDF reports
python paper/generate_pdf.py
python paper/generate_laya_pdf.py
python paper/generate_email_pdf.py
python paper/generate_agentic_pdf.py
```

---

## 📜 Citations

```bibtex
@article{talreja2026main,
  title={Beyond Generative Overhead: Evaluating System-One Decision Models vs. Frontier LLMs and Open-Weight Encoders},
  author={Talreja, Shrey},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}

@article{talreja2026agentic_pipeline,
  title={Autonomous Code Vulnerability Triage, Threat Analysis, and Patch Remediation via Local Multi-Stage Agentic Pipelines},
  author={Talreja, Shrey},
  journal={GitHub Repository: shreytalreja25/jev-vs-the-world},
  year={2026}
}
```
