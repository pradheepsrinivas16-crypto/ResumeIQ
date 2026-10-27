CAREER_TRACKS = {
    "Data Engineer": {"python", "sql", "etl", "spark", "pipeline", "aws", "database", "airflow", "kafka", "pandas"},
    "Machine Learning Engineer": {"python", "machine learning", "pytorch", "tensorflow", "deep learning", "docker", "nlp", "scikit-learn"},
    "Backend / Platform Engineer": {"python", "fastapi", "django", "rest", "docker", "microservices", "sql", "redis", "postgresql", "git"},
    "Data Analyst / BI Specialist": {"sql", "tableau", "power bi", "excel", "visualization", "analytics", "dashboard", "python", "statistics"},
    "DevOps / Cloud Specialist": {"docker", "kubernetes", "ci/cd", "terraform", "aws", "linux", "cloud", "git", "bash"},
    "Full Stack Developer": {"javascript", "react", "html", "css", "node", "python", "sql", "api", "git"}
}

def get_alternative_pathways(resume_skills):
    """Calculate transferable fit scores for adjacent career specializations."""
    matched_skills_list = [str(s).lower() for s in (resume_skills or [])]
    recommendations = []

    for role_name, required_techs in CAREER_TRACKS.items():
        overlap = [t for t in required_techs if any(t in s for s in matched_skills_list)]
        calc_score = int((len(overlap) / max(len(required_techs), 1)) * 100)
        if calc_score >= 15:
            recommendations.append({
                "role": role_name,
                "fit": min(calc_score + 25, 96),
                "skills": overlap[:5]
            })

    return sorted(recommendations, key=lambda x: x["fit"], reverse=True)[:3]