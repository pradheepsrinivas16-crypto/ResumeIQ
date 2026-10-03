from resume_parser import extract_resume_text
from job_matcher import calculate_match_score


# -----------------------------------------
# 1. Load resume
# -----------------------------------------

resume_path = "Pradeep_Srinivas_Resume_ATS (1).pdf"  # Change this to your actual resume file

resume_text = extract_resume_text(resume_path)


# -----------------------------------------
# 2. Example job description
# -----------------------------------------

job_description = """
We are looking for a Data Analyst who can work with
Python, SQL, Power BI, Excel, data visualization,
data cleaning, exploratory data analysis, and
statistical analysis.

The candidate should be able to analyze datasets,
create dashboards, track KPIs, and communicate
business insights to stakeholders.
"""


# -----------------------------------------
# 3. Calculate match score
# -----------------------------------------

score = calculate_match_score(
    resume_text,
    job_description
)


# -----------------------------------------
# 4. Display result
# -----------------------------------------

print("\n======================================")
print("       JOB MATCHING RESULT")
print("======================================")

print(f"Semantic Match Score: {score:.2f}%")

print("======================================")