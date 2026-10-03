from pathlib import Path
import sys

# Allow imports from src/
sys.path.append(str(Path(__file__).resolve().parent))

from resume_parser import extract_resume_text
from skill_matcher import compare_skills


# ============================================================
# FILE PATH
# ============================================================
resume_path = Path(
    r"C:\Users\pradh\Downloads\Pradeep_Srinivas_Resume_ATS (1).pdf"
)


# ============================================================
# CHECK FILE
# ============================================================

if not resume_path.exists():

    print("\nERROR: Resume PDF not found.")
    print("Expected location:")
    print(resume_path)

    sys.exit(1)


# ============================================================
# EXTRACT RESUME
# ============================================================

resume_text = extract_resume_text(
    resume_path
)


# ============================================================
# TEST JOB DESCRIPTION
# ============================================================

job_description = """
We are looking for a Data Analyst.

Required skills:

Python
SQL
Excel
Power BI
Tableau
Data Visualization
Machine Learning
Statistics
Dashboard Development
Data Analysis
"""


# ============================================================
# COMPARE SKILLS
# ============================================================

result = compare_skills(
    resume_text,
    job_description
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("REAL RESUME SKILL MATCHING TEST")
print("=" * 60)


print("\nResume Skills:")
for skill in result["resume_skills"]:
    print("  ✓", skill)


print("\nRequired Skills:")
for skill in result["required_skills"]:
    print("  •", skill)


print("\nMatched Skills:")
for skill in result["matched_skills"]:
    print("  ✓", skill)


print("\nMissing Skills:")
for skill in result["missing_skills"]:
    print("  ✗", skill)


print("\nSkill Evidence:")

for skill, evidence in result["skill_evidence"].items():

    print(
        f"  {skill}: "
        f"{evidence['evidence']}"
    )


# ============================================================
# SUMMARY
# ============================================================

required_count = len(
    result["required_skills"]
)

matched_count = len(
    result["matched_skills"]
)

if required_count > 0:

    skill_score = (
        matched_count /
        required_count
    ) * 100

else:

    skill_score = 0


print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(
    f"Required Skills : {required_count}"
)

print(
    f"Matched Skills  : {matched_count}"
)

print(
    f"Missing Skills  : "
    f"{len(result['missing_skills'])}"
)

print(
    f"Skill Coverage  : "
    f"{skill_score:.2f}%"
)

print("=" * 60)