from src.resume_parser import extract_resume_text
from src.skill_matcher import compare_skills

resume_text = extract_resume_text("Karan Resume.pdf")

job_description = """
We are looking for a Full Stack Developer.

Required Skills:
- HTML
- CSS
- JavaScript
- React
- Spring Boot
- MySQL
- REST API
- Git

Responsibilities:
- Develop responsive web applications.
- Build frontend interfaces using React.
- Develop backend APIs using Spring Boot.
- Work with MySQL databases.
- Integrate frontend and backend services.
- Test and debug applications.
"""

result = compare_skills(resume_text, job_description)

print("\n=== REQUIRED SKILLS ===")
print(result["required_skills"])

print("\n=== MATCHED SKILLS ===")
print(result["matched_skills"])

print("\n=== RELATED SKILLS ===")
print(result["related_skills"])

print("\n=== MISSING SKILLS ===")
print(result["missing_skills"])

print("\n=== EVIDENCE LEVELS ===")
for skill, evidence in result["skill_evidence_levels"].items():
    print(skill, "=>", evidence)
    print("\n=== REQUIRED SKILL EVIDENCE ===")

for skill, evidence in result["required_skill_evidence_levels"].items():
    print(skill, "=>", evidence)