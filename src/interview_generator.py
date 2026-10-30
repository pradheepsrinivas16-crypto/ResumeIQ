"""
Smart Recruiter Interview Question Generator
Dynamically crafts screening questions tailored to candidate fit, gap severity, and verified competencies.
"""

from src.skill_matcher import format_skill_display

BASIC_MISSING_QUESTIONS = {
    "git": "What branching strategies (e.g., GitFlow, feature branches) and commands do you use for collaborative source control?",
    "ci/cd": "Have you worked with any automated build or CI/CD pipelines (e.g., GitHub Actions, Jenkins) to test and deploy applications?",
    "node.js": "How does the Node.js event-driven, non-blocking I/O model work, and when would you choose it over multi-threaded architectures?",
    "django": "Can you explain how the Django ORM handles migrations and database relationships?",
    "fastapi": "How does FastAPI handle dependency injection and automatic OpenAPI documentation generation?",
    "rest api": "How do you handle asynchronous HTTP responses, client-side status-code handling (e.g., 404 vs 500), and response parsing when consuming RESTful APIs?",
    "react": "Can you explain how state updates work in React, and when you would use useState versus passing props down a component hierarchy?",
    "sql": "Can you describe what relational databases you have interacted with, and what basic SELECT, WHERE, and JOIN queries you have written?",
    "excel": "In your coursework or projects, how have you used Microsoft Excel to organize, calculate, or filter data tables?",
    "power bi": "Have you used Power BI or any other BI tool to create basic visual charts or connect to an Excel/CSV data source?",
    "dashboard": "Can you share an example of a visual report or dashboard you developed to present findings to classmates or stakeholders?",
    "pandas": "Have you worked with Python Pandas to load CSV data and inspect DataFrames using functions like .head(), .describe(), or .info()?",
    "numpy": "How have you used NumPy arrays or basic mathematical functions in your Python coursework?",
    "database": "What experience do you have creating or querying database tables using SQL or other database management software?",
    "data analysis": "Can you walk through a project where you took raw numbers and analyzed them to answer a specific question?",
    "data visualization": "Which charting tools (e.g., Matplotlib, Excel, Tableau) have you used to communicate data visually?",
    "kpi": "How do you define a Key Performance Indicator (KPI), and can you give an example of one you tracked in a project?",
    "exploratory data analysis": "What steps do you take when first opening a new dataset to inspect data types, missing values, and distributions?",
    "statistical analysis": "What basic statistical concepts (such as mean, median, standard deviation, or correlation) have you applied to analyze data?"
}

JD_CENTRALITY = [
    "rest api", "git", "ci/cd", "node.js", "django", "fastapi", "react", "sql", "power bi",
    "javascript", "html", "css", "dashboard", "data analysis", "python", "excel",
    "responsive web design", "ui/ux", "figma", "adobe xd", "database", "exploratory data analysis",
    "pandas", "numpy", "kpi", "statistical analysis"
]

def generate_interview_questions(missing_skills, substituted_skills=None, supporting_skills=None, listed_skills=None, demonstrated_skills=None, final_score=100.0):
    questions = []
    missing_skills = [str(s).strip().lower() for s in (missing_skills or [])]
    substituted_skills = substituted_skills or {}
    supporting_skills = [str(s).strip().lower() for s in (supporting_skills or [])]
    listed_skills = [str(s).strip().lower() for s in (listed_skills or [])]
    demonstrated_skills = [str(s).strip().lower() for s in (demonstrated_skills or [])]

    # FILTER: Remove abstract database terms from missing and substitute lists
    filtered_missing = [s for s in missing_skills if s not in {"database", "sql"}]
    
    # 1. Missing requirements prioritized by JD centrality
    sorted_missing = sorted(filtered_missing, key=lambda s: JD_CENTRALITY.index(s) if s in JD_CENTRALITY else 99)
    for skill in sorted_missing[:2]:
        q_text = BASIC_MISSING_QUESTIONS.get(
            skill,
            f"The job specifies {format_skill_display(skill)}, which was not verified on your resume. Could you describe any academic projects, labs, or coursework where you used this technology?"
        )
        questions.append({
            "category": f"Gap Validation ({format_skill_display(skill)})",
            "type": "Missing Requirement",
            "question": q_text
        })

    # 2. Tool transitions for concrete substitutes only
    for target_skill, sub_tool in substituted_skills.items():
        if len(questions) >= 5:
            break
        # Guard: Never generate transitions into abstract "Database" or "SQL"
        if target_skill in {"database", "sql", "mongodb", "mysql", "postgresql"}:
            continue
        
        target_disp = format_skill_display(target_skill)
        sub_disp = format_skill_display(sub_tool)
        
        if target_skill in {"tableau", "power bi"}:
            asset_phrase = "reporting models and dashboards"
        elif target_skill in {"figma", "adobe xd"}:
            asset_phrase = "wireframes and design components"
        else:
            asset_phrase = "workflows and codebases"

        questions.append({
            "category": f"Tooling Transition ({sub_disp} → {target_disp})",
            "type": "Tool Adaptation",
            "question": f"You've used {sub_disp} in projects, while our role specifies {target_disp}. How comfortable are you translating your {asset_phrase} into {target_disp}?"
        })

    # 3. Supporting skills probe
    for skill in supporting_skills:
        if len(questions) >= 5:
            break
        disp = format_skill_display(skill)
        questions.append({
            "category": f"Experience Verification ({disp})",
            "type": "Supporting Skill Verification",
            "question": f"You have {disp} listed under your internship or educational experience. What specific features, interfaces, or deliverables did you build with {disp} during that period?"
        })

    # 4. Listed skills probe
    for skill in listed_skills:
        if len(questions) >= 5:
            break
        if skill in {"database", "sql"}:
            continue
        disp = format_skill_display(skill)
        questions.append({
            "category": f"Depth Verification ({disp})",
            "type": "Listed-Only Skill",
            "question": f"You have {disp} listed in your technical competencies without an explicit project bullet point. Can you describe an academic project or task where you applied {disp}?"
        })

    return questions[:5]