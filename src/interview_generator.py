"""
Smart Recruiter Interview Question Generator
Generates targeted technical questions based on candidate evidence levels,
substitutions, and unverified skill gaps.
"""

CURATED_GAP_QUESTIONS = {
    "rest api": [
        "How do you typically structure asynchronous HTTP client handling and error boundaries when consuming RESTful APIs in a frontend framework?",
        "Can you walk us through how you handle API authentication (such as JWT tokens) and state hydration in modern web applications?"
    ],
    "react": [
        "Can you explain your approach to state management when scaling a React application—specifically when choosing between Context API, custom hooks, or external stores?",
        "How do you optimize render performance in React components that handle frequent updates or large lists?"
    ],
    "git": [
        "Describe your preferred Git branching strategy for collaborative features and how you resolve complex merge conflicts in production branches.",
        "How do you use interactive rebasing, stashing, or cherry-picking to maintain a clean commit history?"
    ],
    "sql": [
        "Walk us through a scenario where you had to optimize a slow-running SQL query. What indexing strategies or execution plan analyses did you apply?",
        "How do you approach writing complex analytical queries involving window functions versus subqueries?"
    ],
    "python": [
        "How do you ensure memory efficiency and speed when processing large datasets with Python?",
        "Can you describe your experience structuring modular, testable Python code using object-oriented principles or functional paradigms?"
    ],
    "docker": [
        "How do you design multi-stage Docker builds to keep production image sizes minimal and secure?",
        "Can you describe how you configure environment variables and volume persistence across local and containerized environments?"
    ]
}

def generate_interview_questions(missing_skills, substituted_skills=None, listed_skills=None):
    """
    Generates a structured list of interview questions tailored to the candidate's screening profile.
    """
    questions = []
    substituted_skills = substituted_skills or {}
    listed_skills = listed_skills or []

    # 1. Questions targeting unverified or missing skills (Priority 1)
    for skill in missing_skills:
        skill_norm = str(skill).strip().lower()
        if skill_norm in CURATED_GAP_QUESTIONS:
            for q in CURATED_GAP_QUESTIONS[skill_norm]:
                questions.append({
                    "category": f"Gap Validation ({skill.title()})",
                    "type": "Missing Requirement",
                    "question": q
                })
        else:
            questions.append({
                "category": f"Gap Validation ({skill.title()})",
                "type": "Missing Requirement",
                "question": f"The job requires hands-on experience with {skill.title()}, which was not explicitly verified on your resume. Could you describe any recent projects or theoretical understanding you have with this technology?"
            })

    # 2. Questions evaluating substitute tooling transitions (Priority 2)
    for target_skill, sub_tool in substituted_skills.items():
        questions.append({
            "category": f"Tooling Transition ({sub_tool.title()} → {target_skill.title()})",
            "type": "Tool Adaptation",
            "question": f"You demonstrated strong production proficiency in {sub_tool.title()}, while our role specifies {target_skill.title()}. How comfortable are you translating your workflow and component structures into {target_skill.title()}?"
        })

    # 3. Questions verifying depth for listed-only skills (Priority 3)
    for skill in listed_skills[:2]:
        questions.append({
            "category": f"Depth Verification ({skill.title()})",
            "type": "Listed-Only Skill",
            "question": f"You have {skill.title()} listed in your technical competencies without an explicit project bullet point. Can you share a concrete production problem where you applied {skill.title()}?"
        })

    return questions