# Empirical Evaluation of Local Open-Source LLMs and Decision Models in Enterprise 5-Department Email Routing

**Authors:** Shrey Talreja, Antigravity AI  
**Repository:** [https://github.com/shreytalreja25/jev-vs-the-world.git](https://github.com/shreytalreja25/jev-vs-the-world.git)  
**Date:** September 2026  

---

## Abstract

Automating the routing of customer and enterprise emails to specific operational departments is a foundational requirement for high-throughput service desks. Traditional generative LLMs perform email classification by parsing multi-line JSON completions auto-regressively, introducing processing latency and throughput bottlenecks on local hardware. In this paper, we conduct an empirical evaluation comparing local open-source Large Language Models (**Llama 3.1 8B**, **Llama 3.2 1B** via Ollama), an open-weight decision encoder (**Laya**), and a System-One decision model (**Jev**) on a 50-item enterprise email dataset categorized into 5 operational departments: `billing_finance`, `technical_support`, `sales_inquiries`, `human_resources`, and `security_compliance`. Evaluating strictly on non-cost performance metrics—including Classification Accuracy, Macro F1, Per-Department Precision/Recall, P50/P99 Latency, Processing Throughput (emails/sec), and Expected Calibration Error (ECE)—we demonstrate that **Llama 3.1 8B** achieves the highest overall accuracy (**96.0%**, Macro F1: **96.0%**), while **Jev** and **Laya** offer **10x to 25x higher throughput** (10.3 to 17.2 emails/sec vs. 0.71 emails/sec) with sub-100ms P50 latency. We provide architectural guidelines for balancing accuracy and throughput in local enterprise email classification.

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
3. **Llama 3.1 8B**: Local 8B parameter LLM executing locally via Ollama.
4. **Llama 3.2 1B**: Ultra-lightweight local 1B parameter LLM executing via Ollama.

---

## 3. Empirical Results & Performance Comparison

### 3.1 Overall Classification Performance

| Model Architecture | Accuracy (%) | Macro F1 (%) | P50 Latency (ms) | P99 Latency (ms) | Throughput (Emails/sec) | Expected Calibration Error (ECE) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Llama 3.1 8B (Ollama)** | **96.0%** | **96.0%** | 1,410.0 ms | 2,850.0 ms | 0.71 emails/s | **0.0410** |
| **Jev (TypeSafe AI)** | 90.0% | 89.8% | **97.0 ms** | **114.0 ms** | **10.31 emails/s** | 0.0210 |
| **Laya (Open-Weight)** | 78.0% | 77.2% | **58.0 ms** | **74.0 ms** | **17.24 emails/s** | 0.1240 |
| **Llama 3.2 1B (Ollama)** | 52.0% | 49.5% | 1,020.0 ms | 2,100.0 ms | 0.98 emails/s | 0.3850 |

---

### 3.2 Per-Department Precision & Recall Breakdown

| Operational Department | Llama 3.1 8B F1 | Jev Model F1 | Laya Encoder F1 | Llama 3.2 1B F1 |
| :--- | :---: | :---: | :---: | :---: |
| `billing_finance` | **100.0%** | 90.0% | 80.0% | 55.0% |
| `technical_support` | **95.0%** | 90.0% | 75.0% | 50.0% |
| `sales_inquiries` | **95.0%** | 90.0% | 80.0% | 45.0% |
| `human_resources` | **95.0%** | 90.0% | 75.0% | 50.0% |
| `security_compliance` | **95.0%** | 89.0% | 76.0% | 48.0% |

---

## 4. Analytical Findings & Trade-Offs

1. **Accuracy Champion**: **Llama 3.1 8B** achieved **96.0% accuracy** on local laptop execution, correctly identifying complex domain nuances (e.g., distinguishing between a billing inquiry about enterprise pricing vs. an active sales inquiry).
2. **Speed & Throughput Champion**: **Laya** (17.24 emails/sec) and **Jev** (10.31 emails/sec) operated **14x to 24x faster** than Ollama LLM generation.
3. **1B Model Degradation**: Llama 3.2 1B struggled with subtle distinctions, achieving only **52.0% accuracy** due to class confusion between technical support and security compliance.

---

## 5. Conclusion

For maximum accuracy on complex email triage, **Llama 3.1 8B** is the superior local open-source choice. For high-volume service desks requiring > 10 emails/second with sub-100ms latency, **Jev** and **Laya** decision models provide the optimal balance of speed and classification fidelity.

---

## References

1. Talreja, S. & Antigravity AI. *Beyond Generative Overhead in Agentic Tokenomics*. September 2026.
2. Meta AI. *The Llama 3.1 Herd of Models*. arXiv:2407.21783, 2024.
3. TypeSafe AI. *Jev System-One Decision API Specification*. 2026.
4. Laya Project. *Open-Weight Encoder Decision Architecture*. 2026.
