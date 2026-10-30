"""
Smart Recruiter Interview Question Generator
Dynamically crafts screening questions tailored to candidate fit and gap severity.
"""

from src.skill_matcher import format_skill_display

# Basic fundamental screening questions for missing skills
BASIC_MISSING_QUESTIONS = {
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

# In-depth technical questions for demonstrated or listed skills
DEPTH_QUESTIONS = {
    "excel": "In your data workflows, when would you use an XLOOKUP or INDEX/MATCH versus structuring data into an Excel Pivot Table or Data Model?",
    "pandas": "When cleaning messy datasets in Pandas, how do you handle missing values using .fillna() or .dropna(), and how do you avoid chained indexing warnings?",
    "rest api": "How do you handle asynchronous HTTP responses, status code error handling, and state hydration when consuming RESTful APIs?",
    "sql": "Can you explain the difference between a WHERE clause and a HAVING clause when aggregating records in SQL, and when you would use window functions?",
    "power bi": "How do you structure data relationships in Power BI (star schema vs snowflake), and what is your approach to writing performant DAX measures?",
    "python": "How do you choose between list comprehensions, generator expressions, and built-in functions like map/filter when optimizing memory for large datasets?"
}

# Centrality priority order for JDs
JD_CENTRALITY = [
    "sql", "power bi", "dashboard", "data analysis", "excel", 
    "python", "data visualization", "kpi", "database", 
    "exploratory data analysis", "pandas", "statistical analysis", "numpy"
]

def generate_interview_questions(missing_skills, substituted_skills=None, listed_skills=None, demonstrated_skills=None, final_score=100.0):
    questions = []
    missing_skills = [str(s).strip().lower() for s in (missing_skills or [])]
    substituted_skills = substituted_skills or {}
    listed_skills = [str(s).strip().lower() for s in (listed_skills or [])]
    demonstrated_skills = [str(s).strip().lower() for s in (demonstrated_skills or [])]

    # Rule: If candidate fit is below 35%, recommend against full interview loop
    if final_score < 35.0:
        sorted_gaps = sorted(missing_skills, key=lambda s: JD_CENTRALITY.index(s) if s in JD_CENTRALITY else 99)
        top_3 = sorted_gaps[:3]
        for skill in top_3:
            q_text = BASIC_MISSING_QUESTIONS.get(
                skill,
                f"The job requires foundational exposure to {format_skill_display(skill)}. What coursework or academic lab projects have you completed in this area?"
            )
            questions.append({
                "category": f"Core Gap ({format_skill_display(skill)})",
                "type": "Advisory Screening Question",
                "question": q_text
            })
        return questions

    # 1. Prioritize missing skills by JD centrality
    sorted_missing = sorted(missing_skills, key=lambda s: JD_CENTRALITY.index(s) if s in JD_CENTRALITY else 99)
    for skill in sorted_missing[:3]:
        q_text = BASIC_MISSING_QUESTIONS.get(
            skill,
            f"The job specifies {format_skill_display(skill)}, which was not verified on your resume. Could you describe any academic projects, labs, or coursework where you used this technology?"
        )
        questions.append({
            "category": f"Gap Validation ({format_skill_display(skill)})",
            "type": "Missing Requirement",
            "question": q_text
        })

    # 2. Tool transitions for substitutes
    for target_skill, sub_tool in substituted_skills.items():
        if len(questions) >= 5:
            break
        questions.append({
            "category": f"Tooling Transition ({format_skill_display(sub_tool)} → {format_skill_display(target_skill)})",
            "type": "Tool Adaptation",
            "question": f"You demonstrated strong proficiency in {format_skill_display(sub_tool)}, while our role specifies {format_skill_display(target_skill)}. How comfortable are you translating your workflow and assets into {format_skill_display(target_skill)}?"
        })

    # 3. Depth verification for listed-only skills
    for skill in listed_skills:
        if len(questions) >= 5:
            break
        if skill in DEPTH_QUESTIONS:
            questions.append({
                "category": f"Depth Verification ({format_skill_display(skill)})",
                "type": "Listed-Only Skill",
                "question": DEPTH_QUESTIONS[skill]
            })
        else:
            questions.append({
                "category": f"Depth Verification ({format_skill_display(skill)})",
                "type": "Listed-Only Skill",
                "question": f"You have {format_skill_display(skill)} listed in your technical competencies without an explicit project bullet point. Can you describe an academic project or internship task where you applied {format_skill_display(skill)}?"
            })

    # 4. If no gaps exist, add deep-dive project verification questions
    if not missing_skills and demonstrated_skills:
        if ("data analysis" in demonstrated_skills or "python" in demonstrated_skills) and len(questions) < 5:
            questions.append({
                "category": "Project Deep-Dive (Cricket-Twin AI)",
                "type": "Project Verification",
                "question": "In your Cricket-Twin AI project, what specific algorithmic logic did you build yourself for the match performance simulator versus relying on pre-existing packages?"
            })
        if ("power bi" in demonstrated_skills or "dashboard" in demonstrated_skills) and len(questions) < 5:
            questions.append({
                "category": "Project Deep-Dive (BI Dashboards)",
                "type": "Project Verification",
                "question": "In your Power BI dashboard project, what specific DAX calculations or data transformations did you implement to track stakeholder KPIs?"
            })

    # Strict hard cap at 5 questions
    return questions[:5]