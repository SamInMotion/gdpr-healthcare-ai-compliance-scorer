# GDPR Healthcare AI Compliance Scorer

Ontology-first, rules-first framework for assessing GDPR compliance in healthcare AI systems.

---

## Overview

The **GDPR Healthcare AI Compliance Scorer** is a modular project designed to **assess AI systems for GDPR compliance**, specifically within healthcare contexts. It provides:

* **Evidence-based scoring** of documents against GDPR requirements.
* **Reproducible test cases** using synthetic data.
* A framework that bridges **research experimentation** and **practical industry compliance verification**.
* **Ontology + rules first approach**: requirements are explicitly modeled as rules, not hidden in ML models.
* A **Streamlit-based UI** for interactive exploration and exporting compliance reports.

The project is open-source to encourage collaboration and ensure **full transparency and reproducibility**.

---
## Scope & Limitations
This beta release is focused on English-language privacy policies and compliance documentation. 
Support for Norwegian and other languages will be added in future updates.

## Prerequisites

* **Git** for version control.
* **Bash** or a Unix-like shell for command execution.
* **Python 3.x** (currently using 3.13) for running scoring logic.
* **Dependencies:**

  * [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) for extracting text from PDFs.
  * [PyYAML](https://pyyaml.org/) for loading compliance rules.
  * [Streamlit](https://streamlit.io/) for interactive UI and visualization.

---

## Project Setup

1. **Initialize repository**

```bash
git init
```

2. **Create directories**

```bash
mkdir test_docs reports
```

3. **Add scoring pipeline**

```bash
mkdir -p pipeline/scoring
touch pipeline/scoring/__init__.py
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Synthetic Test Documents for Article 9

* **10 synthetic text documents** (`doc1.txt` – `doc10.txt`) under `test_docs/`.
* **Content focus:** Simulated healthcare scenarios relevant to **Article 9: Processing of special categories of personal data**.
* Additional reference document: **CELEX\_32016R0679\_EN\_TXT\_GDPR.pdf** (GDPR text).

---

## Rule-Based Scoring (Article 9)

1. **Rules file (`article9.yaml`)**

   * Each clause of Article 9 is defined as a human-readable rule (`A9_1`, `A9_2a`, … `A9_4`).
   * Rules specify `description`, `keywords`, and `weight`.

2. **Scorer (`article9_scorer.py`)**

   * Loads YAML rules and applies them to extracted text.
   * Produces:

     * **Score (0–100%)**
     * **Compliance level** (✅ High, ⚠️ Partial, ❌ Non-compliant)
     * **Requirements met/failed**
     * **Warnings for critical prohibitions**

3. **Streamlit App (`app.py`)**

   * Upload and score PDFs interactively.
   * Displays:

     * Compliance score
     * Passed/failed requirements
     * Priority actions
   * Allows exporting results to Markdown reports under `reports/`.

---

## Example Run

Run via command line:

```bash
python -m pipeline.scoring.test_all_pdfs
```

Run with UI:

```bash
streamlit run app.py
```

Sample Streamlit output:

```
Compliance Score: 42/42 (100%)
Requirements Met: 13
Requirements Failed: 0
Compliance Level: ✅ High Compliance
Priority Actions: No high-priority issues found!
```

Generated Markdown report (example):

```
# GDPR Article 9 Compliance Report

**Document:** CELEX_32016R0679_EN_TXT_GDPR.pdf  
**Date:** 2025-09-20 13:25:24

**Score:** 42 / 42 (100%)  
**Compliance Level:** ✅ High Compliance  

## Breakdown
- Requirements Met: 13
- Requirements Failed: 0
- Priority Actions: None
```

---

## Rationale for This Approach

1. **Synthetic + Real PDFs:** Ensures controlled testing while validating pipeline robustness.
2. **Ontology + Rules First:** Keeps compliance **explicit and explainable**.
3. **Streamlit UI:** Enables interactive analysis and quick validation.
4. **Reports:** Standardized Markdown export for traceability.
5. **Pipeline modularity:** Easy to extend beyond Article 9 (e.g., EU AI Act, MDR, anti-corruption).

---

## Next Steps

* Add **multi-format report generation** (JSON/CSV/HTML/PDF).
* Expand pipeline with **additional GDPR articles**.
* Introduce **modular compliance packs** (EU AI Act, MDR, anti-corruption).
* Enable **fine-grained evidence tracing** (text spans linked to rule matches).
* Improve UI with **charts and filtering options**.

---



