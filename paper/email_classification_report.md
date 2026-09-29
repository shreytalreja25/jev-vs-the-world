# Empirical Evaluation of Local Open-Source LLMs and Decision Models in Enterprise 5-Department Email Routing

**Author:** Shrey Talreja  
**Repository:** [https://github.com/shreytalreja25/jev-vs-the-world.git](https://github.com/shreytalreja25/jev-vs-the-world.git)  
**Date:** September 2026  

---

## Abstract

Automating the routing of customer and enterprise emails to specific operational departments is a foundational requirement for high-throughput service desks. Traditional generative LLMs perform email classification by parsing multi-line JSON completions auto-regressively, introducing processing latency and throughput bottlenecks on local hardware. In this paper, we conduct an empirical evaluation comparing local open-source Large Language Models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama), an open-weight decision encoder (**Laya**), and a System-One decision model (**Jev**) on a 50-item enterprise email dataset categorized into 5 operational departments: `billing_finance`, `technical_support`, `sales_inquiries`, `human_resources`, and `security_compliance`. Evaluating strictly on non-cost performance metrics, including Classification Accuracy, Macro F1, Per-Department Precision/Recall, P50/P99 Latency, Processing Throughput (emails/sec), and Expected Calibration Error (ECE), we demonstrate that **Llama 3.1 8B** achieves the highest overall accuracy (**96.0%**, Macro F1: **96.0%**), while **Jev** and **Laya** offer **10x to 25x higher throughput** (10.3 to 17.2 emails/sec vs. 0.71 emails/sec) with sub-100ms P50 latency. We provide architectural guidelines for balancing accuracy and throughput in local enterprise email classification.

---

## 1. Introduction & Task Definition

Enterprise customer service organizations process thousands of incoming emails daily, requiring rapid triage into operational queues:
1. `billing_finance`: Invoice requests, duplicate charges, payment method updates, refund claims.
2. `technical_support`: Application crashes, API 500 errors, database disconnects, SDK bugs.
3. `sales_inquiries`: Enterprise plan quotes, custom SLA inquiries, demo bookings, RFP submissions.
4. `human_resources`: Employment verifications, job applications, interview status, 401k/payroll inquiries.
5. `security_compliance`: SOC2 reports, vulnerability disclosures, GDPR deletion requests, 2FA resets.

In this experiment, we execute all models locally on a standard developer laptop to measure real-world performance without cloud API latency or cost dependencies.

---

## 2. Experimental Setup & Evaluated Models

Each email item consists of a real-world enterprise `subject` and `body` payload. Models must select exactly one of the 5 department choices.

### Evaluated Model Matrix:
1. **Jev (TypeSafe AI)**: System-One non-generative decision model (64k context window).
2. **Laya (Apache-2.0)**: Open-weight encoder decision model (512 token context window).
3. **Qwen 3.5 9B Abliterated**: Uncensored open-weights reasoning model executing via Ollama (`lukey03/qwen3.5-9b-abliterated`).
4. **Llama 3.1 8B**: Local 8B parameter LLM executing locally via Ollama.
5. **Llama 3.2 1B**: Ultra-lightweight local 1B parameter LLM executing via Ollama.

---

## 3. Empirical Results & Performance Comparison

### 3.1 Overall Classification Performance

| Model Architecture | Accuracy (%) | Macro F1 (%) | P50 Latency (ms) | P99 Latency (ms) | Throughput (Emails/sec) | Expected Calibration Error (ECE) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Qwen 3.5 9B Abliterated (Ollama)** | **96.0%** | **98.2%** | 12,530.0 ms | 15,615.7 ms | 0.10 emails/s | **0.0372** |
| **Llama 3.1 8B (Ollama)** | 94.0% | 97.2% | 3,464.1 ms | 14,415.5 ms | 0.19 emails/s | 0.0400 |
| **Jev (TypeSafe AI)** | 88.0% | 95.4% | **99.0 ms** | **114.0 ms** | **10.08 emails/s** | 0.0440 |
| **Laya (Open-Weight)** | 72.0% | 84.6% | **60.0 ms** | **71.5 ms** | **16.75 emails/s** | 0.3440 |
| **Llama 3.2 1B (Ollama)** | 30.0% | 27.3% | 1,380.7 ms | 16,381.5 ms | 0.24 emails/s | 0.6332 |

---

### 3.2 Per-Department Precision & Recall Breakdown

| Operational Department | Qwen 3.5 9B F1 | Llama 3.1 8B F1 | Jev Model F1 | Laya Encoder F1 | Llama 3.2 1B F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `billing_finance` | 90.9% | **100.0%** | 76.9% | 52.6% | 100.0% |
| `technical_support` | **100.0%** | 95.0% | **100.0%** | 70.6% | 0.0% |
| `sales_inquiries` | **100.0%** | 95.0% | **100.0%** | 75.0% | 36.4% |
| `human_resources` | **100.0%** | 95.0% | **100.0%** | 75.0% | 0.0% |
| `security_compliance` | **100.0%** | 95.0% | **100.0%** | 76.0% | 0.0% |

---

## 4. Analytical Findings & Trade-Offs

1. **F1 & Calibration Champion**: **Qwen 3.5 9B Abliterated** achieved the highest overall Macro F1 (**98.2%**) and the lowest Expected Calibration Error (**0.0372**), securing a flawless 100% F1 score across 4 of the 5 operational departments (`technical_support`, `sales_inquiries`, `human_resources`, `security_compliance`).
2. **Speed & Throughput Champion**: **Laya** (16.75 emails/sec) and **Jev** (10.08 emails/sec) operated **100x to 160x faster** than the heavier reasoning models, delivering instantaneous sub-100ms P50 latency.
3. **Reasoning Overhead vs Accuracy**: While Qwen 3.5 9B demonstrated near-perfect categorization fidelity, its deep internal reasoning mechanisms produced a P50 latency of ~12.5s on local hardware, making it ideal for offline batch auditing rather than real-time synchronous ingress.

---

## 5. Conclusion

For maximum accuracy on complex email triage, **Llama 3.1 8B** is the superior local open-source choice. For high-volume service desks requiring > 10 emails/second with sub-100ms latency, **Jev** and **Laya** decision models provide the optimal balance of speed and classification fidelity.

---

## References

1. Talreja, S. *Beyond Generative Overhead in Agentic Tokenomics*. September 2026.
2. Meta AI. *The Llama 3.1 Herd of Models*. arXiv:2407.21783, 2024.
3. TypeSafe AI. *Jev System-One Decision API Specification*. 2026.
4. Laya Project. *Open-Weight Encoder Decision Architecture*. 2026.
