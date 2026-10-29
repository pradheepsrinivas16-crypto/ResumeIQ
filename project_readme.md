# ResumeIQ

**Deep Learning-Based Resume Screening and Job Recommendation System**

ResumeIQ is an explainable resume intelligence platform that analyzes candidate resumes against target job descriptions. It combines calibrated dense semantic embeddings, 4-tier evidence-weighted skill verification, fine-tuned BERT domain classification, capability intelligence, automated recruiter interview generation, and exportable decision-support briefs.

> **Important:** ResumeIQ is an augmented decision-support system. Its compatibility score is a heuristic compatibility index and should not be used as the sole determinant for automated employment decisions.

---

## 🌟 What's New in v1.1.0

- **4-Tier Evidence Hierarchy:** Distinguishes between Demonstrated work experience ($1.00\times$), Valid Tool Substitutions ($0.75\times$), Supporting education/certifications ($0.70\times$), and Listed-Only skills ($0.40\times$).
- **Calibrated Semantic Similarity:** Piecewise scaling maps raw MiniLM cosine similarity to an intuitive 15%–95% scale, eliminating semantic compression.
- **💼 Smart Recruiter Interview Question Generator:** Automatically generates targeted technical interview questions tailored to candidate gaps, tool transitions, and listed-only competencies.
- **🏆 Multi-Resume Batch Leaderboard:** Upload and rank entire candidate pools simultaneously against benchmark JDs with dynamic score cutoffs and CSV exports.
- **📄 Candidate Intelligence Brief:** Single-page PDF export generated via ReportLab synchronized with UI metrics, verified evidence snippets, and recommendations.
- **Strict Canonical Equivalence:** Bidirectional tool mapping (e.g., Figma $\leftrightarrow$ Adobe XD, PostgreSQL $\leftrightarrow$ MySQL, Tableau $\leftrightarrow$ Power BI).

---

## Project Overview

ResumeIQ accepts a **PDF or DOCX resume** and a **job description** and produces:

- **Overall Compatibility Score** (Calibrated Semantic Alignment 60% + Evidence-Weighted Skill Coverage 40%)
- **4-Tier Skill Evidence Drill-Down** with quoted sentences from experience and project sections
- **Smart Recruiter Technical Interview Questions** for candidate gaps and tooling transitions
- **High-Level Capability Engine** with alignment coverage metrics across engineering disciplines
- **Job Responsibility & Action Verbs Matcher** with direct textual evidence
- **Cross-Functional Career Pathways** (JD-independent market transferability)
- **Auxiliary BERT Domain Classification** (Segment Vote Share)
- **ATS Bullet-Point Optimizer** addressing verified candidate gaps

The application is built as an interactive Streamlit dashboard with core Python NLP/ML engines in `src/`.

---

## System Architecture

```text
Resume (PDF/DOCX)
        |
        v
Resume Parser (PyPDF / python-docx)
        |
        v
Clean Resume Text & Section Hierarchy
        |
        +----------------------------------------+
        |                                        |
        v                                        v
Calibrated Semantic Engine             4-Tier Evidence Skill Engine
MiniLM Embeddings + Cosine Mapping     Canonical Taxonomy + Section Evidence
        |                                        |
        v                                        v
Calibrated Semantic Score (60%)        Evidence Skill Score (40%)
        |                               (Demonstrated / Sub / Listed / Missing)
        +-------------------+--------------------+
                            |
                            v
              Final Compatibility Score
                            |
        +-------------------+--------------------+
        |                   |                    |
        v                   v                    v
Fine-tuned BERT       Capability Engine     Smart Interview Generator
Domain Classifier     Requirement Coverage  Dynamic Technical Inquiries
        |                   |                    |
        +-------------------+--------------------+
                            |
                            v
            Dual-Mode Streamlit Dashboard
            (Single Deep-Dive & Batch Leaderboard)
                            |
                            v
          Synchronized PDF Intelligence Brief
```

---

## Core Components

### 1. Resume Parsing
`src/resume_parser.py`
- PDF extraction using `pypdf` with page-level fault tolerance.
- DOCX parsing using `python-docx` with paragraph and table extraction.
- Section detector separating Experience, Projects, Education, Certifications, and Skills.

### 2. Calibrated Semantic Matching
`src/job_matcher.py`
- Embeddings generated via `sentence-transformers/all-MiniLM-L6-v2`.
- Raw cosine similarity across dense resume text typically falls within a compressed range ($0.15$ to $0.55$).
- A piecewise calibration function maps raw scores into an intuitive, human-interpretable range ($15\%$ to $95\%$) without distorting rank order.

### 3. Evidence-Weighted Skill Intelligence
`src/skill_matcher.py`
Uses a taxonomy covering 100+ canonical technical competencies with alias resolution and word-boundary regex. Skills are evaluated against an evidence ladder:
- **Demonstrated ($1.00\times$):** Verified in active work experience, internship, or project delivery sentences.
- **Substitute Tool ($0.75\times$):** Canonical industry equivalence (e.g., Figma for Adobe XD, PostgreSQL for MySQL).
- **Supporting ($0.70\times$):** Verified in certifications, coursework, or education.
- **Listed-Only ($0.40\times$):** Detected strictly in standalone skills lists or document fallback without project context.
- **Missing ($0.00\times$):** No evidence detected.

### 4. Compatibility Scoring Formula
$$\text{Final Compatibility} = (\text{Calibrated Semantic Score} \times 0.60) + (\text{Evidence Skill Coverage} \times 0.40)$$

Where Skill Coverage ties out to:
$$\text{Skill Coverage (\%)} = \frac{(\text{Demonstrated} \times 1.0) + (\text{Substitute} \times 0.75) + (\text{Supporting} \times 0.70) + (\text{Listed} \times 0.40)}{\text{Total Required Skills}} \times 100$$

### 5. Smart Recruiter Interview Question Generator
`src/interview_generator.py`
Dynamically crafts technical interview questions during screening calls:
- **Gap Validation:** Architectural questions for missing requirements (e.g., REST API, React).
- **Tool Adaptation:** Questions assessing workflow transitions for substitute tools (e.g., Figma $\rightarrow$ Adobe XD).
- **Depth Verification:** Implementation-depth questions for skills claimed only in the skills list.

### 6. Job Responsibility & Action Engine
`src/screening_engine.py`
- Extracts explicit duty headings or falls back to engineering action verbs (`Build`, `Develop`, `Query`, `Design`) for paragraph JDs.
- Deduplicates substrings and matches verified claims against candidate experience text.

### 7. Capability & Career Intelligence
`src/capability_engine.py` & `src/career_paths.py`
- Aggregates atomic skills into grouped engineering competencies (Frontend, UI/UX, API Development, Full Stack, Version Control, Data Analytics) with alignment classifications.
- Evaluates transferable competencies against global market profiles independent of the target JD.

### 8. Auxiliary BERT Domain Classification
`src/bert_category_predictor.py`
- Fine-tuned BERT model classifying candidate resumes into 24 Kaggle dataset categories.
- Evaluated via segmented token voting across document windows and reported as **Segment Vote Share**.
- Operates strictly as an auxiliary predictor without modifying the deterministic 60/40 score.

---

## 📊 Benchmark Validation

The engine was audited and benchmarked across diverse technical domains:

| Scenario | Candidate Profile | Target Job Description | Calibrated Semantic | Evidence Skill Coverage | Final Compatibility | Outcome |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Data In-Domain Fit** | **Pradeep** (Data Analyst) | Data Analyst JD | 93.0% | 88.0% | **91.0%** | 🟢 Strong Fit (Rank #1) |
| **Frontend In-Domain Fit** | **Karan** (Frontend Dev) | Frontend Developer JD | 65.5% | 87.5% | **74.3%** | 🟢 Solid Fit (1 Gap: REST API) |
| **Cross-Domain Separation** | **Pradeep** (Data Analyst) | Frontend Developer JD | 49.5% | 16.0% | **36.1%** | 🔴 Rejection (Web Skills Missing) |

---

# Deep Learning Experiments

The project was developed as a comparative NLP/DL study rather than relying on a single model.

## Resume Classification Results

Evaluation artifacts are stored under `data/evaluation/`.

| Model | Test Accuracy | Weighted F1 |
|---|---:|---:|
| TF-IDF + SVM | 72.12% | 71.00% |
| Sentence Transformer + SVM | 74.80% | 73.00% |
| CNN | 67.83% | 64.00% |
| LSTM | 10.72% | 10.00% |
| BERT | 79.36% | 77.38% |

These are classification results on the project's held-out test set. They should not be interpreted as hiring or job-fit accuracy.

## Semantic Matching Experiments

A separate semantic matching comparison evaluated different representations on the compatibility benchmark.

| Model | Accuracy | Spearman Correlation |
|---|---:|---:|
| TF-IDF + Cosine | 57.50% | 0.8849 |
| MiniLM + Cosine | 85.00% | 0.9099 |
| BERT + Cosine | 60.00% | 0.7079 |

This experiment supports the current architectural separation:
- **BERT** → resume category classification
- **MiniLM** → resume/JD semantic similarity
- **Skill taxonomy** → explicit 4-tier skill evidence and coverage

---

# Compatibility Evaluation

The repository contains a manually labelled 40-pair compatibility benchmark (`data/evaluation/compatibility_test_set.csv`).

Benchmark distribution:
- **Good:** 16
- **Partial:** 13
- **Poor:** 11
- **Total:** 40 pairs

The resulting **82.50% classification accuracy** demonstrates that the compatibility pipeline reliably distinguishes structured compatibility tiers.

---

# Repository Structure

```text
ResumeIQ/
│
├── app.py                         # Streamlit UI (Single Deep-Dive & Batch Leaderboard)
├── requirements.txt               # Production dependencies
├── README.md                      # Project documentation
├── .gitignore
│
├── data/
│   └── evaluation/                # Model comparison benchmarks & confusion matrices
│
└── src/
    ├── bert_category_predictor.py # Segmented BERT sequence classifier
    ├── bullet_generator.py        # ATS-formatted bullet point optimizer
    ├── capability_engine.py       # High-level capability rules & coverage
    ├── career_paths.py            # Universal market transferability pathways
    ├── interview_generator.py     # Smart recruiter interview question generator
    ├── job_matcher.py             # Calibrated MiniLM semantic matcher
    ├── pdf_generator.py           # ReportLab candidate brief generator
    ├── recommendations.py         # Explainable score interpretation
    ├── resume_parser.py           # PDF and DOCX text extractor
    ├── role_suitability.py        # Curated standard role matching
    ├── screening_engine.py        # Dual-engine orchestrator & responsibility parser
    ├── skill_matcher.py           # Taxonomy, evidence classifier & canonical mapping
    └── styles.py                  # Custom Streamlit UI CSS injection
```

---

## Getting Started

### 1. Create and Activate Virtual Environment

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run ResumeIQ

```powershell
python -m streamlit run app.py
```

---

# Technology Stack

- **Application & Dashboard:** Streamlit, ReportLab (PDF Export), Pandas
- **Core Languages & Libraries:** Python 3.10+, PyTorch, Regex
- **NLP & Transformers:** `sentence-transformers/all-MiniLM-L6-v2`, Hugging Face Transformers (`bert-base-uncased`)
- **Machine Learning & Evaluation:** Scikit-learn, NumPy, Matplotlib
- **Document Processing:** `pypdf`, `python-docx`

---

# Responsible AI & Ethical Hiring Notice

ResumeIQ is designed strictly as an augmented decision-support system. Compatibility scores, BERT classifications, and detected capabilities are heuristic indicators. Automated employment rejections or hiring choices should never be made solely on algorithmic outputs. Human review remains essential in all hiring processes.

---

# Project Status

**Current status: v1.1.0 Production-Ready Release**

All evidence leaks, equivalence mappings, scoring arithmetic tie-outs, and multi-tier classifications have been verified across real-world candidate benchmarks.