"""
Cross-Functional Career Pathways (Broad Market Transferability)
Dynamically recomputed from candidate evidence levels (Demonstrated: 1.0x, Supporting: 0.70x, Listed: 0.40x).
"""

from src.skill_matcher import format_skill_display

CAREER_TRACKS = {
    "Full Stack Developer": {
        "skills": ["javascript", "html", "css", "react", "angular", "node.js", "spring boot", "java", "sql", "git"],
        "gate_frontend": {"javascript", "html", "react", "angular"},
        "gate_backend": {"spring boot", "node.js", "fastapi", "django", "java", "python"},
        "min_skills": 3
    },
    "Data Analyst / BI Specialist": {
        "skills": ["sql", "tableau", "power bi", "excel", "data visualization", "data analysis", "dashboard", "python", "kpi"],
        "gate": {"sql", "power bi", "tableau", "excel", "data analysis"},
        "min_skills": 3
    },
    "Data Engineer": {
        "skills": ["python", "sql", "etl", "database", "pandas", "aws", "data engineering", "spark"],
        "gate": {"python", "sql", "database"},
        "min_skills": 3
    },
    "Backend / Platform Engineer": {
        "skills": ["java", "spring boot", "python", "fastapi", "sql", "rest api", "docker", "node.js", "git"],
        "gate": {"spring boot", "fastapi", "django", "java", "node.js", "rest api"},
        "min_skills": 3
    },
    "Machine Learning Engineer": {
        "skills": ["python", "machine learning", "deep learning", "scikit-learn", "pytorch", "tensorflow", "data analysis"],
        "gate": {"machine learning", "deep learning", "scikit-learn", "pytorch", "tensorflow"},
        "min_skills": 3
    }
}

EVIDENCE_WEIGHTS = {
    "demonstrated": 1.00,
    "substitute": 0.75,
    "supporting": 0.70,
    "listed": 0.40,
    "listed_only": 0.40,
    "missing": 0.00
}

def get_alternative_pathways(resume_skills, skill_evidence_levels=None):
    """
    Computes market transferability dynamically based on actual evidence tier weights.
    Demonstrated = 1.0x, Supporting = 0.70x, Listed Only = 0.40x.
    """
    matched_skills_set = {str(s).lower().strip() for s in (resume_skills or []) if str(s).strip()}
    ev_levels = skill_evidence_levels or {}
    recommendations = []

    for role_name, config in CAREER_TRACKS.items():
        track_skills = config["skills"]
        
        # Hard discipline gating
        if "gate" in config:
            if not matched_skills_set.intersection(config["gate"]):
                continue

        if "gate_backend" in config:
            has_fe = bool(matched_skills_set.intersection(config["gate_frontend"]))
            has_be = bool(matched_skills_set.intersection(config["gate_backend"]))
            if not (has_fe and has_be):
                continue

        overlap = [s for s in track_skills if s in matched_skills_set]
        if len(overlap) < config.get("min_skills", 2):
            continue

        # Dynamic tier-weighted score
        earned_points = 0.0
        for s in overlap:
            ev = ev_levels.get(s, {})
            status = str(ev.get("status", "listed")).strip().lower()
            earned_points += EVIDENCE_WEIGHTS.get(status, 0.40)

        # Base transferability coverage
        coverage_pct = (earned_points / len(track_skills)) * 100.0
        
        # Market transferability calibration: scaled proportionally from verified evidence
        fit_score = int(min(coverage_pct * 1.25 + 15.0, 95.0))

        if fit_score >= 25:
            recommendations.append({
                "role": role_name,
                "fit": fit_score,
                "skills": overlap[:5]
            })

    recommendations.sort(key=lambda x: (-x["fit"], x["role"]))
    return recommendations[:3]