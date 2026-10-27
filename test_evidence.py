from src.resume_parser import extract_resume_text
from src.skill_matcher import classify_skill_evidence

resume_text = extract_resume_text("Karan Resume.pdf")

skills = [
    "python",
    "power bi",
    "sql",
    "html",
    "css",
    "javascript",
    "react"
]

for skill in skills:
    result = classify_skill_evidence(resume_text, skill)
    print(f"{skill} => {result}")