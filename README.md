# GDPR Healthcare AI Compliance Scorer

Ontology-first, rules-first framework for assessing GDPR compliance in healthcare AI systems.

---

## Overview

The **GDPR Healthcare AI Compliance Scorer** is a modular project designed to **assess AI systems for GDPR compliance**, specifically within healthcare contexts. It provides:

* **Evidence-based scoring** of documents against GDPR requirements.
* **Reproducible test cases** using synthetic data.
* A framework that bridges **research experimentation** and **practical industry compliance verification**.
* **Ontology + rules first approach**: requirements are explicitly modeled as rules, not hidden in ML models.

The project is open-source to encourage collaboration and ensure **full transparency and reproducibility**.

---

## Prerequisites

* **Git** for version control.
* **Bash** or a Unix-like shell for command execution.
* **Python 3.x** (currently using 3.13) for running scoring logic.
* **Dependencies:**

  * [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) for extracting text from PDFs.
  * [PyYAML](https://pyyaml.org/) for loading compliance rules.

**Rationale:** These tools ensure reproducibility, modular design, and human-readable rule definitions.

---

## Project Setup

1. **Initialize repository**

```bash
git init
```

*Establishes version control to track all changes and maintain reproducibility.*

2. **Create directories**

```bash
mkdir test_docs
```

*Organizes synthetic test documents separately from code for clarity and modularity.*

3. **Add scoring pipeline**

```bash
mkdir -p pipeline/scoring
touch pipeline/scoring/__init__.py
```

*Creates a modular scoring package that can be extended to other GDPR articles later.*

---

## Synthetic Test Documents for Article 9

* **10 synthetic text documents** (`doc1.txt` – `doc10.txt`) created under `test_docs/`.
* **Content focus:** Simulated healthcare scenarios relevant to **Article 9: Processing of special categories of personal data**.

**Git workflow:**

```bash
git add test_docs/*.txt
git commit -m "Add 10 synthetic test documents for Article 9 compliance scoring"
git push
```

*Rationale: Establishes a **baseline dataset** for reproducible testing without exposing real patient data.*

---

## Rule-Based Scoring (Article 9)

1. **Rules file (`article9_rules.yaml`)**

   * Defines each clause of Article 9 as **human-readable rules** (`A9_1`, `A9_2a`, … `A9_4`).
   * Each rule contains:

     * **description** (plain-language text of requirement)
     * **keywords** (used for lightweight matching in extracted text)
     * **weight** (importance in final scoring)

*Rationale:* YAML keeps rules transparent, editable, and version-controllable.

2. **Scorer (`article9_scorer.py`)**

   * Loads YAML rules.
   * Extracts text from PDF with **PyMuPDF**.
   * Checks text against rules.
   * Produces:

     * **Score (normalized to 0–100%)**
     * **Compliance level** (✅ High, ⚠️ Partial, ❌ Non-compliant)
     * **Passed / failed requirements**
     * **Warnings for critical prohibitions**

3. **Test runner (`test_all_pdfs.py`)**

   * Iterates through PDFs in `test_docs/`.
   * Runs Article 9 scorer.
   * Prints structured results.

---

## Example Run

```bash
python -m pipeline.scoring.test_all_pdfs
```

Output:

```
--- Scoring PDF: CELEX_32016R0679_EN_TXT_GDPR.pdf ---
Score: 42 / 42
Percentage: 100%
Compliance Level: ✅ High Compliance
Passed requirements: ['A9_1', ..., 'A9_4']
Failed requirements: []

--- Scoring PDF: Intergrating NLP with Computer Vision.pdf ---
Score: 0 / 42
Percentage: 0%
Compliance Level: ❌ Non-Compliant - Major Issues
Passed requirements: []
Failed requirements: ['A9_1']
Warnings:
  - ⚠️ Critical: prohibition - Processing of personal data revealing racial or ethnic origin ...
```

---

## Rationale for This Approach

1. **Synthetic + Real PDFs:** Allows controlled testing while validating pipeline robustness.
2. **Ontology + Rules First:** Keeps compliance **explicit and explainable**.
3. **Normalization:** Ensures scores are always interpretable as **percentages (0–100%)**.
4. **Warnings:** Highlight critical prohibitions separately from general scoring.
5. **Pipeline modularity:** Easy to extend beyond Article 9 (e.g., EU AI Act, MDR, anti-corruption).

---

## Next Steps

* Add **report generation** (JSON/CSV/HTML) for results.
* Expand pipeline with **additional GDPR articles**.
* Introduce **modular compliance packs** (EU AI Act, MDR, anti-corruption).
* Enable **fine-grained evidence tracing** (text spans linked to rule matches).

---

