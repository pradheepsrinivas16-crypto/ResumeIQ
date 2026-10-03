from resume_parser import extract_resume_text
from screening_engine import screen_resume


# ======================================
# RESUME FILE
# ======================================

resume_path = "Pradeep_Srinivas_Resume_ATS (1).pdf"
# Extract resume text
resume_text = extract_resume_text(resume_path)


# ======================================
# JOB DESCRIPTION
# ======================================

print("\n======================================")
print("          JOB DESCRIPTION")
print("======================================")
print("Paste the job description.")
print("Press Enter twice when finished.")
print()

job_lines = []

while True:
    line = input()

    if line.strip() == "":
        break

    job_lines.append(line)

job_description = "\n".join(job_lines)


# ======================================
# SCREEN RESUME
# ======================================

result = screen_resume(
    resume_text,
    job_description
)


# ======================================
# SCREENING REPORT
# ======================================

print("\n======================================")
print("       RESUME SCREENING REPORT")
print("======================================")

print(f"\nFinal Match Score: {result['final_score']:.2f}%")

print(f"Semantic Score: {result['semantic_score']:.2f}%")

print(f"Skill Match Score: {result['skill_score']:.2f}%")


# ======================================
# DISTILBERT CATEGORY
# ======================================

print(
    f"\nPredicted Resume Category: "
    f"{result['category']}"
)

print(
    f"Category Confidence: "
    f"{result['category_confidence']:.2f}%"
)


# ======================================
# REQUIRED SKILLS
# ======================================

print("\nRequired Skills:")
print(result["required_skills"])


# ======================================
# MATCHED SKILLS
# ======================================

print("\nMatched Skills:")
print(result["matched_skills"])


# ======================================
# MISSING SKILLS
# ======================================

print("\nMissing Skills:")
print(result["missing_skills"])


# ======================================
# RESUME SKILLS
# ======================================

print("\nResume Skills:")
print(result["resume_skills"])

print("\n======================================")
print("       RECOMMENDATIONS")
print("======================================")

print("\n💪 Strengths:")

for strength in result["strengths"]:
    print("✓", strength)


print("\n⚠️ Skill Gaps:")

for gap in result["skill_gaps"]:
    print("✗", gap)


print("\n💡 Improvement Suggestions:")

for suggestion in result["suggestions"]:
    print("•", suggestion)


print("\n======================================")