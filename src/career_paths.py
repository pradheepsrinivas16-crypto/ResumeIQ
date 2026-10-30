"""
Cross-Functional Career Pathways
Evaluates overall candidate skills against global market role profiles (JD-Independent).
Enforces hard architectural gating so full-stack tracks are not recommended without
both client-side and server-side framework competencies.
"""

CAREER_TRACKS = {
    "Data Analyst / BI Specialist": {
        "skills": {"sql", "tableau", "power bi", "excel", "visualization", "data analysis", "dashboard", "python", "statistical analysis", "kpi"},
        "min_overlap": 3
    },
    "Data Engineer": {
        "skills": {"python", "sql", "etl", "spark", "aws", "database", "pandas", "data engineering"},
        "min_overlap": 3
    },
    "Machine Learning Engineer": {
        "skills": {"python", "machine learning", "pytorch", "tensorflow", "deep learning", "docker", "nlp", "scikit-learn"},
        "gate": {"machine learning", "deep learning", "scikit-learn", "pytorch", "tensorflow"},
        "min_overlap": 3
    },
    "Backend / Platform Engineer": {
        "skills": {"python", "fastapi", "django", "rest api", "docker", "sql", "redis", "postgresql", "git", "spring boot", "java"},
        "gate": {"fastapi", "django", "rest api", "spring boot", "node.js"},
        "min_overlap": 3
    },
    "Full Stack Developer": {
        "skills": {"javascript", "react", "html", "css", "node.js", "python", "sql", "rest api", "git"},
        "gate_frontend": {"javascript", "html", "react"},
        "gate_backend": {"node.js", "spring boot", "fastapi", "django", "rest api"},
        "min_overlap": 4
    },
    "DevOps / Cloud Specialist": {
        "skills": {"docker", "kubernetes", "ci/cd", "aws", "linux", "cloud", "git", "azure", "gcp"},
        "gate": {"docker", "kubernetes", "aws", "azure", "ci/cd"},
        "min_overlap": 3
    }
}

def get_alternative_pathways(resume_skills):
    """
    Calculate transferable fit scores for adjacent career specializations.
    Applies discipline gating and returns strictly sorted, deterministic results.
    """
    matched_skills_set = {str(s).lower().strip() for s in (resume_skills or []) if str(s).strip()}
    recommendations = []

    for role_name, config in CAREER_TRACKS.items():
        required_techs = config["skills"]
        
        # Hard gate check
        if "gate" in config:
            if not matched_skills_set.intersection(config["gate"]):
                continue

        # Full Stack dual-gate check
        if "gate_backend" in config:
            has_fe = bool(matched_skills_set.intersection(config["gate_frontend"]))
            has_be = bool(matched_skills_set.intersection(config["gate_backend"]))
            if not (has_fe and has_be):
                continue

        overlap = sorted(list(required_techs.intersection(matched_skills_set)))
        if len(overlap) < config.get("min_overlap", 2):
            continue

        raw_percentage = int((len(overlap) / max(len(required_techs), 1)) * 100)
        fit_score = min(raw_percentage + 20, 95)

        recommendations.append({
            "role": role_name,
            "fit": fit_score,
            "skills": overlap[:5]
        })

    # Sort deterministically: highest fit first, then alphabetical by role name
    recommendations.sort(key=lambda x: (-x["fit"], x["role"]))
    return recommendations[:3]