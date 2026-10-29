"""
Smart Recruiter Interview Question Generator
Tailors technical questions to candidate evidence levels, gaps, and claimed competencies.
"""

CURATED_SPECIFIC_QUESTIONS = {
    "excel": "In your data workflows, when would you use an XLOOKUP or INDEX/MATCH versus structuring data into an Excel Pivot Table or Data Model?",
    "pandas": "When cleaning messy datasets in Pandas, how do you handle missing values using .fillna() or .dropna(), and how do you avoid chained indexing warnings?",
    "rest api": "How do you handle asynchronous HTTP responses, status code error handling, and state hydration when consuming RESTful APIs in a frontend framework?",
    "react": "Can you explain when you would choose React Context API versus external state management, and how you prevent unnecessary component re-renders?",
    "sql": "Can you explain the difference between a WHERE clause and a HAVING clause when aggregating records in SQL, and when you would use window functions?",
    "python": "How do you choose between Python list comprehensions, generator expressions, and built-in functions like map/filter when optimizing memory for large datasets?",
    "power bi": "How do you structure data relationships in Power BI (star schema vs snowflake), and what is your approach to writing performant DAX measures?",
    "git": "Walk us through how you resolve a Git merge conflict when collaborating on a team feature branch, and what your preferred branching strategy is."
}

def generate_interview_questions(missing_skills, substituted_skills=None, listed_skills=None, demonstrated_skills=None):
    questions = []
    substituted_skills = substituted_skills or {}
    listed_skills = listed_skills or []
    demonstrated_skills = demonstrated_skills or []

    # 1. Questions targeting unverified or missing skills (Priority 1)
    for skill in missing_skills:
        skill_norm = str(skill).strip().lower()
        if skill_norm in CURATED_SPECIFIC_QUESTIONS:
            questions.append({
                "category": f"Gap Validation ({skill.title()})",
                "type": "Missing Requirement",
                "question": CURATED_SPECIFIC_QUESTIONS[skill_norm]
            })
        else:
            questions.append({
                "category": f"Gap Validation ({skill.title()})",
                "type": "Missing Requirement",
                "question": f"The job requires hands-on experience with {skill.title()}, which was not verified on your resume. Could you describe any academic projects, labs, or coursework where you used this technology?"
            })

    # 2. Questions evaluating substitute tooling transitions (Priority 2)
    for target_skill, sub_tool in substituted_skills.items():
        questions.append({
            "category": f"Tooling Transition ({sub_tool.title()} → {target_skill.title()})",
            "type": "Tool Adaptation",
            "question": f"You demonstrated strong proficiency in {sub_tool.title()}, while our role specifies {target_skill.title()}. How comfortable are you translating your workflow, styles, and assets into {target_skill.title()}?"
        })

    # 3. Depth verification for listed-only skills (Priority 3)
    for skill in listed_skills[:2]:
        skill_norm = str(skill).strip().lower()
        if skill_norm in CURATED_SPECIFIC_QUESTIONS:
            questions.append({
                "category": f"Depth Verification ({skill.title()})",
                "type": "Listed-Only Skill",
                "question": CURATED_SPECIFIC_QUESTIONS[skill_norm]
            })
        else:
            questions.append({
                "category": f"Depth Verification ({skill.title()})",
                "type": "Listed-Only Skill",
                "question": f"You have {skill.title()} listed in your technical competencies without an explicit project bullet point. Can you describe an academic project or internship task where you applied {skill.title()}?"
            })

    # 4. If no gaps exist, add deep-dive project verification questions
    if not missing_skills and demonstrated_skills:
        if "data analysis" in demonstrated_skills or "python" in demonstrated_skills:
            questions.append({
                "category": "Project Deep-Dive (Cricket-Twin AI)",
                "type": "Project Verification",
                "question": "In your Cricket-Twin AI project, what specific algorithmic logic did you build yourself for the match performance simulator versus relying on pre-existing packages?"
            })
        if "power bi" in demonstrated_skills or "dashboard" in demonstrated_skills:
            questions.append({
                "category": "Project Deep-Dive (BI Dashboards)",
                "type": "Project Verification",
                "question": "In your Power BI dashboard project, what specific DAX calculations or data transformations did you implement to track stakeholder KPIs?"
            })

    return questions