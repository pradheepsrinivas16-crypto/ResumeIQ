# ResumeIQ

**Deep Learning-Based Resume Screening and Job Recommendation System**

ResumeIQ is a resume intelligence application that analyzes a candidate resume against a target job description. It combines semantic similarity, explicit skill matching, fine-tuned BERT resume classification, capability analysis, and evidence-based recommendations.

> **Important:** ResumeIQ is a decision-support prototype. Its compatibility score is not a hiring probability and should not be used as the sole basis for employment decisions.

## Project Overview

ResumeIQ accepts a **PDF or DOCX resume** and a **job description** and produces:

- Overall compatibility score
- Semantic compatibility score
- Skill coverage score
- Matched and missing skills
- BERT-based resume category classification
- Higher-level capability analysis
- Candidate strengths
- Skill gaps and improvement suggestions
- Transparent score explanation

The application is built as a Streamlit interface with Python NLP/ML components in the `src/` directory.

## System Architecture

```text
Resume (PDF/DOCX)
        |
        v
Resume Parser
        |
        v
Clean Resume Text
        |
        +------------------------------+
        |                              |
        v                              v
Semantic Matching                Skill Intelligence
MiniLM embeddings                Skill taxonomy + aliases
        |                              |
        |                              v
        |                       Matched / Missing Skills
        |                              |
        v                              v
Semantic Score                 Skill Coverage Score
        |                              |
        +---------------+--------------+
                        |
                        v
              Compatibility Score
              60% Semantic
              40% Skill Coverage
                        |
        +---------------+----------------+
        |                                |
        v                                v
 Fine-tuned BERT                  Capability Engine
 Resume Classification            Evidence-based capability rules
        |                                |
        v                                v
 Top Resume Categories             Capability Evidence
        |
        +-------------------+
                            |
                            v
                 Recommendations
                 + Explanation
                            |
                            v
                    Streamlit UI
```

## Core Components

### 1. Resume Parsing

`src/resume_parser.py`

Supports:

- PDF resumes using PyPDF
- DOCX resumes using python-docx
- Text extraction and basic cleaning
- PDF page-level error handling
- DOCX table extraction

### 2. Semantic Matching

`src/job_matcher.py`

Uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Cosine similarity

The resume and job description are converted into embeddings and compared to produce the semantic compatibility score.

### 3. Skill Intelligence

`src/skill_matcher.py`

Uses a professional skill taxonomy with canonical skills and aliases.

Current taxonomy includes areas such as:

- Programming: Python, Java, C, C++, JavaScript, TypeScript
- Web: HTML, CSS, React, Node.js, FastAPI, Flask, Django
- Databases: SQL, MySQL, PostgreSQL, MongoDB, Redis
- Data Science: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
- ML/DL: Machine Learning, Deep Learning, NLP, Computer Vision
- ML Engineering: MLOps, Model Deployment, Model Serving
- Cloud: AWS, Azure, Google Cloud, Cloud Computing
- DevOps: Docker, Kubernetes, CI/CD, Jenkins, Linux
- Version Control: Git, GitHub, GitLab
- BI: Excel, Power BI, Tableau, Dashboard, KPI
- Other: TensorFlow, PyTorch, OpenCV, Spark, Hadoop, GraphQL

Matching uses normalized text, aliases, and regex word boundaries to avoid simple substring false matches.

### 4. Compatibility Score

The current compatibility score is calculated as:

```text
Compatibility Score =
    Semantic Score × 0.60
    +
    Skill Coverage × 0.40
```

Skill coverage is:

```text
Skill Coverage =
    Matched Required Skills
    ----------------------- × 100
    Total Required Skills
```

The 60/40 weighting is an engineering design choice for this prototype; it has not been established as a universal hiring-validity formula.

### 5. Fine-Tuned BERT Classification

`src/bert_category_predictor.py`

The project includes a fine-tuned BERT model for classifying resumes into the 24 categories represented in the Kaggle Resume Dataset.

BERT classification is **separate from compatibility scoring**.

Its confidence represents the model's probability distribution across resume categories. It is not a hiring probability and does not affect the compatibility score.

### 6. Capability Intelligence

`src/capability_engine.py`

The capability engine maps detected resume skills to higher-level capabilities using explicit core/supporting evidence rules.

Current capabilities:

- Data Science
- Data Analytics
- Machine Learning
- Business Intelligence
- Data Visualization

Capability results are evidence-based rule outputs and do not change the compatibility score.

### 7. Recommendations

`src/recommendations.py`

Generates:

- Candidate strengths
- Skill gaps
- Improvement suggestions
- Score interpretation

Recommendations are based on detected skills and compatibility components rather than an LLM making an opaque hiring decision.

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
- **Skill taxonomy** → explicit skill coverage and evidence

The BERT classifier was not reused as the semantic similarity model because its classification-oriented representation performed worse on the project's semantic matching benchmark.

---

# Compatibility Evaluation

The repository contains a manually labelled 40-pair compatibility benchmark:

`data/evaluation/compatibility_test_set.csv`

The current compatibility pipeline was evaluated using the real screening engine.

### Current benchmark result

- **40 labelled resume/JD pairs**
- Good: 16
- Partial: 13
- Poor: 11
- Overall classification accuracy: **82.50%**

The benchmark uses three labels:

- `good`
- `partial`
- `poor`

Current score interpretation in the evaluation script:

- `>= 70` → good
- `50–69.99` → partial
- `< 50` → poor

This is a small manually labelled proof-of-concept benchmark, not a production hiring validation study. Partial examples show overlap with the score thresholds, so further evaluation with a larger and independently labelled dataset would be valuable.

---

# Dataset

The original resume classification experiments used the Kaggle Resume Dataset.

Project preprocessing:

```text
Original resumes: 2,484
Clean resumes:    2,481
Categories:       24
```

The cleaned dataset was split using stratification:

```text
Training:   1,736
Validation:   372
Test:         373
```

The raw and processed datasets are intentionally excluded from this GitHub repository.

---

# Repository Structure

```text
ResumeIQ/
│
├── app.py
├── .gitignore
│
├── data/
│   └── evaluation/
│       ├── bert_classification_report.csv
│       ├── bert_confusion_matrix.csv
│       ├── bert_confusion_matrix.png
│       ├── bert_confusion_matrix_final.png
│       ├── bert_prediction_check.csv
│       ├── compatibility_results.csv
│       ├── compatibility_test_set.csv
│       ├── final_model_comparison.csv
│       ├── model_accuracy_comparison.png
│       ├── semantic_matching_comparison.csv
│       ├── semantic_matching_comparison.png
│       └── ...
│
└── src/
    ├── bert_category_predictor.py
    ├── bert_prediction_check.py
    ├── capability_engine.py
    ├── category_predictor.py
    ├── compare_semantic_matchers.py
    ├── contextual_skill_matcher.py
    ├── evaluate_compatibility.py
    ├── final_bert_evaluation.py
    ├── job_matcher.py
    ├── model_comparison.py
    ├── recommendations.py
    ├── resume_parser.py
    ├── screening_engine.py
    ├── semantic_skill_matcher.py
    ├── skill_matcher.py
    ├── split_dataset.py
    ├── train_bert_svm.py
    ├── train_cnn.py
    ├── train_lstm.py
    ├── train_tfidf_svm.py
    └── test_*.py
```

## Running the Application

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

The current source imports packages including:

```text
streamlit
sentence-transformers
scikit-learn
pandas
numpy
torch
transformers
joblib
pypdf
python-docx
matplotlib
```

Install the required packages in your environment before running the application.

### 3. Run ResumeIQ

```powershell
python -m streamlit run app.py
```

The application opens as a local Streamlit application.

### 4. Use the application

1. Upload a PDF or DOCX resume.
2. Paste a target job description.
3. Click **Analyze Resume Compatibility**.
4. Review:
   - Compatibility score
   - Semantic compatibility
   - Skill coverage
   - Matched skills
   - Missing skills
   - Score explanation
   - Recommendations
   - BERT classification
   - Capability intelligence

---

# Model and Data Files

Large or sensitive artifacts are intentionally excluded through `.gitignore`.

Excluded items include:

- `.venv/`
- `models/`
- raw datasets
- processed datasets
- uploaded PDF/DOCX resumes
- local secrets
- backup Python files

Therefore, the GitHub repository contains the source code and evaluation artifacts, but not the trained model weights or original dataset.

For a complete local reproduction of the BERT classifier, the trained model must be obtained/recreated separately and placed in the expected local model path used by the project.

---

# Evaluation and Reproducibility

The repository contains evaluation scripts and artifacts for:

- Resume classification
- BERT prediction verification
- Confusion matrix generation
- Compatibility evaluation
- Semantic matcher comparison
- Model comparison
- Calibration experiments

Important evaluation files include:

```text
data/evaluation/final_model_comparison.csv
data/evaluation/semantic_matching_comparison.csv
data/evaluation/compatibility_results.csv
data/evaluation/bert_classification_report.csv
data/evaluation/bert_confusion_matrix_final.png
```

---

# Limitations

Current limitations include:

1. The compatibility benchmark contains only 40 manually labelled pairs.
2. The 60/40 compatibility weighting is an engineering choice, not a validated hiring formula.
3. Skill extraction depends on the current predefined taxonomy and aliases.
4. The capability engine is rule-based rather than learned.
5. BERT classification performance varies considerably by resume category, especially for classes with fewer examples.
6. Raw datasets and trained model weights are not included in the public repository.
7. The current system is a prototype and should not be used as an automated employment decision maker.
8. The semantic matcher and skill matcher are separate components; their combination is designed for interpretability rather than claiming a universally optimal formula.

---

# Future Work

Potential next improvements include:

- Larger independently labelled compatibility dataset
- More robust skill/entity extraction
- Better handling of context and negation
- Calibration of compatibility scores
- Additional transformer-based matching experiments
- Better model/version management
- Automated testing and CI
- Production deployment architecture
- More comprehensive explainability
- Evaluation across more diverse resume and job-description datasets

These are development directions rather than claims that the current system already implements them.

---

# Technology Stack

**Frontend / Application**
- Streamlit

**Programming**
- Python

**NLP / Deep Learning**
- PyTorch
- Hugging Face Transformers
- BERT
- Sentence Transformers

**Machine Learning**
- Scikit-learn
- SVM
- TF-IDF
- CNN
- LSTM
- Cosine similarity

**Document Processing**
- PyPDF
- python-docx

**Data / Evaluation**
- Pandas
- NumPy
- Matplotlib

---

# Responsible AI

ResumeIQ is designed as an analytical and educational prototype.

The system should:

- provide evidence for detected skills
- distinguish classification from compatibility
- show missing requirements
- communicate limitations
- avoid presenting compatibility as hiring probability

Human review remains necessary for employment decisions.

---

# Project Status

**Current status: Active prototype / research project**

The current repository represents the working ResumeIQ implementation and its experimental evaluation artifacts. Future development will focus on improving robustness, validation, reproducibility, and production readiness.
