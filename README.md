# X-Flow: Explanation-Augmented Prompting for LLM-Based Intrusion Detection

This repository contains the code, prompts, explanation dataset, and experimental resources associated with the paper:

**X-Flow: Explanation-Augmented Prompting for LLM-Based Intrusion Detection**
Ivan Pizarro, Ricardo Ñanculef, Carlos Valle
Accepted for publication at **IEEE ICPRS 2025** (not yet officially published).

X-Flow is a two-stage methodology that enhances flow-based network intrusion detection by leveraging Large Language Models (LLMs). The approach first extracts class-level natural language explanations from labeled IDS data, and then injects this knowledge into the classification prompt of another LLM. This explanation-guided process significantly improves classification performance compared to zero-shot, few-shot, and recent deep learning baselines.

---

## Repository Structure

```
├── Explanations/                               # Generated class-level explanations (dataset)
├── Predictions/                                # Predictions from the 10-run evaluation
├── Training_set/                               # Samples used during the explanation extraction phase
├── Validation_set/                             # Validation subsets used for evaluation
├── llm_gpt_10run_fewshot.ipynb                 # Few-shot baseline experiments
├── llm_gpt_10run_fewshot_megaprompt.ipynb      # Few-shot with expanded prompts
├── llm_gpt_10run_zeroshot.ipynb                # Zero-shot baseline experiments
└── README.md
```

---

## Overview of X-Flow

X-Flow consists of two main phases:

### **1. Knowledge Extraction**
An LLM generates natural language explanations for multiple examples of each attack class. These explanations are then summarized into a single class-level description.

### **2. Knowledge Injection**
The summarized explanations are embedded into the classification prompt of another LLM, enabling it to use domain-specific knowledge during inference without fine-tuning or continued pre-training.

This method improves macro F1-score by **12.9 to 39.2 points** over zero-shot depending on the model, and also yields more stable predictions than few-shot prompting.

---

## Citation

If you use this repository, the explanation dataset, or any component of the X-Flow methodology in academic work, **please cite the following paper**:

```
@inproceedings{pizarro2025xflow,
title={X-Flow: Explanation-Augmented Prompting for LLM-Based Intrusion Detection},
author={Pizarro, Ivan and Ñanculef, Ricardo and Valle, Carlos},
booktitle={IEEE International Conference on Pattern Recognition Systems (ICPRS)},
year={2025},
note={Accepted, to appear}
}
```
