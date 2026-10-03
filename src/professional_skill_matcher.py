from pathlib import Path
import sys

# ============================================================
# PATH SETUP
# ============================================================

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

sys.path.append(str(SRC_DIR))


# ============================================================
# IMPORTS
# ============================================================

from resume_parser import extract_resume_text
from skill_matcher import compare_skills
from evidence_skill_matcher import analyze_semantic_evidence


# ============================================================
# RESUME PATH
# ============================================================

resume_path = Path(
    r"C:\Users\pradh\Downloads\Pradeep_Srinivas_Resume_ATS (1).pdf"
)

# ============================================================
# CHECK RESUME
# ============================================================

if not resume_path.exists():

    print("\nERROR: Resume not found.")
    print("\nExpected location:")
    print(resume_path)

    sys.exit(1)


# ============================================================
# EXTRACT RESUME
# ============================================================

print("\nExtracting resume...")

resume_text = extract_resume_text(
    resume_path
)

print(
    f"Resume extracted successfully."
)


# ============================================================
# REALISTIC DATA ANALYST JOB DESCRIPTION
# ============================================================

job_description = """

DATA ANALYST

We are looking for a Data Analyst to support
data-driven business decisions.

Responsibilities:

- Analyze business and operational data.
- Clean and preprocess datasets.
- Perform exploratory data analysis.
- Create dashboards and reports.
- Develop data visualizations.
- Identify trends and patterns.
- Communicate analytical findings.

Required Skills:

- Python
- SQL
- Excel
- Power BI
- Tableau
- Data Analysis
- Data Analytics
- Data Visualization
- Statistical Analysis
- Machine Learning
- Dashboard Development
- Data Cleaning
- Exploratory Data Analysis
- Predictive Modeling

Preferred Skills:

- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Git
- GitHub

"""


# ============================================================
# EXACT + ALIAS MATCHING
# ============================================================

exact_result = compare_skills(
    resume_text,
    job_description
)


# ============================================================
# GET RESULTS
# ============================================================

resume_skills = exact_result[
    "resume_skills"
]

required_skills = exact_result[
    "required_skills"
]

exact_matches = exact_result[
    "matched_skills"
]

exact_missing = exact_result[
    "missing_skills"
]


# ============================================================
# REMOVE EXACT MATCHES
# ============================================================

unmatched_required_skills = [
    skill
    for skill in required_skills
    if skill not in exact_matches
]


# ============================================================
# SEMANTIC ANALYSIS
# ============================================================

semantic_result = analyze_semantic_evidence(
    resume_skills,
    unmatched_required_skills
)


# ============================================================
# RESULTS
# ============================================================

high_confidence = semantic_result[
    "high_confidence_matches"
]

review_matches = semantic_result[
    "review_matches"
]

weak_matches = semantic_result[
    "weak_matches"
]


# ============================================================
# DISPLAY REPORT
# ============================================================

print("\n" + "=" * 75)
print("REAL RESUME — PROFESSIONAL SKILL ANALYSIS")
print("=" * 75)


# ============================================================
# RESUME SKILLS
# ============================================================

print("\nRESUME SKILLS DETECTED")

for skill in resume_skills:

    print(
        f"  ✓ {skill}"
    )


# ============================================================
# REQUIRED SKILLS
# ============================================================

print("\nJOB SKILLS DETECTED")

for skill in required_skills:

    print(
        f"  • {skill}"
    )


# ============================================================
# EXACT MATCHES
# ============================================================

print("\nEXACT / ALIAS MATCHES")

if exact_matches:

    for skill in exact_matches:

        print(
            f"  ✓ {skill}"
        )

else:

    print("  None")


# ============================================================
# HIGH CONFIDENCE SEMANTIC
# ============================================================

print(
    "\nHIGH-CONFIDENCE SEMANTIC MATCHES"
)

if high_confidence:

    for match in high_confidence:

        print(
            f"  ✓ "
            f"{match['required_skill']}"
            f" ← "
            f"{match['resume_skill']}"
            f" "
            f"({match['similarity']:.3f})"
        )

else:

    print("  None")


# ============================================================
# REVIEW
# ============================================================

print(
    "\nREVIEW / POSSIBLE RELATED SKILLS"
)

if review_matches:

    for match in review_matches:

        print(
            f"  ? "
            f"{match['required_skill']}"
            f" ← "
            f"{match['resume_skill']}"
            f" "
            f"({match['similarity']:.3f})"
        )

else:

    print("  None")


# ============================================================
# WEAK
# ============================================================

print(
    "\nWEAK / UNMATCHED SEMANTIC RELATIONSHIPS"
)

if weak_matches:

    for match in weak_matches:

        print(
            f"  ✗ "
            f"{match['required_skill']}"
            f" ← "
            f"{match['resume_skill']}"
            f" "
            f"({match['similarity']:.3f})"
        )

else:

    print("  None")


# ============================================================
# CURRENT BASELINE
# ============================================================

required_count = len(
    required_skills
)

matched_count = len(
    exact_matches
)

if required_count > 0:

    baseline_coverage = (
        matched_count /
        required_count
    ) * 100

else:

    baseline_coverage = 0.0


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("BASELINE SUMMARY")
print("=" * 75)

print(
    f"Required Skills : "
    f"{required_count}"
)

print(
    f"Exact/Alias     : "
    f"{len(exact_matches)}"
)

print(
    f"Missing         : "
    f"{len(exact_missing)}"
)

print(
    f"Baseline Skill Coverage : "
    f"{baseline_coverage:.2f}%"
)

print(
    f"High-Confidence Semantic : "
    f"{len(high_confidence)}"
)

print(
    f"Review Relationships     : "
    f"{len(review_matches)}"
)

print(
    f"Weak Relationships       : "
    f"{len(weak_matches)}"
)

print("=" * 75)