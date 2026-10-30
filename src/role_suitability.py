from src.skill_matcher import SKILL_ALIASES

ROLE_PROFILES = {
    "Data Analyst": {
        "core": ["python", "sql", "data analysis", "data visualization"],
        "supporting": ["pandas", "numpy", "excel", "power bi", "statistical analysis", "dashboard"],
    },

    "Business Intelligence Analyst": {
        "core": ["sql", "power bi", "data visualization", "data analysis"],
        "supporting": ["excel", "tableau", "dashboard", "kpi", "python"],
    },

    "Data Scientist": {
        "core": ["python", "machine learning", "data analysis", "statistical analysis"],
        "supporting": ["pandas", "numpy", "scikit-learn", "predictive modeling", "data visualization", "deep learning"],
        "hard_gate": {"machine learning", "scikit-learn", "deep learning", "predictive modeling"}
    },

    "Machine Learning Engineer": {
        "core": ["python", "machine learning", "deep learning"],
        "supporting": ["scikit-learn", "pytorch", "tensorflow", "model deployment", "mlops", "model serving"],
        "hard_gate": {"machine learning", "deep learning", "scikit-learn", "pytorch", "tensorflow"}
    },

    "Frontend Developer": {
        "core": ["html", "css", "javascript"],
        "supporting": ["react", "angular", "typescript", "responsive web design", "ui/ux", "figma", "git"],
        "hard_gate": {"html", "javascript"}
    },

    "Full Stack Developer": {
        # Covers both Modern JS (React/Node) and Enterprise (Java/Spring Boot/Angular)
        "core": ["javascript", "html", "css", "sql"],
        "supporting": ["java", "spring boot", "angular", "react", "node.js", "mysql", "rest api", "git"],
        "hard_gate_frontend": {"html", "javascript", "react", "angular"},
        "hard_gate_backend": {"spring boot", "node.js", "fastapi", "django", "rest api", "java"}
    },

    "Backend Developer": {
        "core": ["java", "spring boot", "rest api"],
        "supporting": ["node.js", "sql", "mysql", "python", "fastapi", "git"],
        "hard_gate": {"spring boot", "node.js", "fastapi", "django", "rest api", "java"}
    },

    "Software Engineer": {
        "core": ["java", "python", "javascript"],
        "supporting": ["sql", "git", "rest api", "data structures"],
    },

    "Mechanical Design Engineer": {
        "core": ["mechanical engineering", "autocad", "solidworks"],
        "supporting": ["catia", "cad", "3d modeling", "gd&t", "manufacturing", "mechanical design"],
    },
}

EVIDENCE_WEIGHTS = {
    "demonstrated": 1.00,
    "supporting": 0.70,
    "substitute": 0.75,
    "listed": 0.40,
    "listed_only": 0.40,
    "missing": 0.00,
}

CORE_WEIGHT = 0.70
SUPPORTING_WEIGHT = 0.30

def canonicalize_resume_skills(resume_skills):
    alias_to_canonical = {}
    for canonical, aliases in SKILL_ALIASES.items():
        alias_to_canonical[canonical.lower().strip()] = canonical
        for alias in aliases:
            alias_to_canonical[alias.lower().strip()] = canonical

    canonical_skills = set()
    for skill in (resume_skills or []):
        normalized = str(skill).lower().strip()
        canonical_skills.add(alias_to_canonical.get(normalized, normalized))

    return canonical_skills

def calculate_role_suitability(resume_skills, role_name, skill_evidence_levels=None):
    if role_name not in ROLE_PROFILES:
        raise ValueError(f"Unknown role: {role_name}")

    profile = ROLE_PROFILES[role_name]
    core_required = set(profile["core"])
    supporting_required = set(profile["supporting"])
    all_required = core_required | supporting_required

    candidate_skills = canonicalize_resume_skills(resume_skills)
    ev_levels = skill_evidence_levels or {}

    matched_skills = sorted(list(candidate_skills.intersection(all_required)))
    missing_skills = sorted(list(all_required - candidate_skills))

    # Hard Gates
    if "hard_gate" in profile and not candidate_skills.intersection(profile["hard_gate"]):
        return {
            "role": role_name,
            "coverage": 32.0,
            "core_coverage": 25.0,
            "supporting_coverage": 40.0,
            "status": "Low Fit",
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "core_matched": sorted(list(candidate_skills.intersection(core_required))),
            "core_missing": sorted(list(core_required - candidate_skills)),
            "supporting_matched": sorted(list(candidate_skills.intersection(supporting_required))),
            "supporting_missing": sorted(list(supporting_required - candidate_skills)),
        }

    if "hard_gate_backend" in profile:
        has_fe = bool(candidate_skills.intersection(profile["hard_gate_frontend"]))
        has_be = bool(candidate_skills.intersection(profile["hard_gate_backend"]))
        if not (has_fe and has_be):
            return {
                "role": role_name,
                "coverage": 35.0,
                "core_coverage": 30.0,
                "supporting_coverage": 45.0,
                "status": "Low Fit",
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "core_matched": sorted(list(candidate_skills.intersection(core_required))),
                "core_missing": sorted(list(core_required - candidate_skills)),
                "supporting_matched": sorted(list(candidate_skills.intersection(supporting_required))),
                "supporting_missing": sorted(list(supporting_required - candidate_skills)),
            }

    def get_evidence_weight(skill):
        if not ev_levels:
            return 1.0 if skill in candidate_skills else 0.0
        ev = ev_levels.get(skill)
        if ev is None:
            for k, v in ev_levels.items():
                if str(k).strip().lower() == skill.lower().strip():
                    ev = v
                    break
        if ev is None:
            return EVIDENCE_WEIGHTS["listed_only"] if skill in candidate_skills else 0.0
        status = str(ev.get("status", "missing")).strip().lower()
        return EVIDENCE_WEIGHTS.get(status, 1.0 if skill in candidate_skills else 0.0)

    if core_required:
        core_score_sum = sum(get_evidence_weight(s) for s in core_required if s in candidate_skills)
        core_score = core_score_sum / len(core_required)
    else:
        core_score = 0.0

    if supporting_required:
        sup_score_sum = sum(get_evidence_weight(s) for s in supporting_required if s in candidate_skills)
        sup_score = sup_score_sum / len(supporting_required)
    else:
        sup_score = 0.0

    weighted_coverage = (core_score * CORE_WEIGHT + sup_score * SUPPORTING_WEIGHT) * 100

    if weighted_coverage >= 80.0:
        status = "Strong Fit"
    elif weighted_coverage >= 50.0:
        status = "Moderate Fit"
    else:
        status = "Low Fit"

    return {
        "role": role_name,
        "coverage": round(weighted_coverage, 1),
        "core_coverage": round(core_score * 100, 1),
        "supporting_coverage": round(sup_score * 100, 1),
        "status": status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "core_matched": sorted(list(candidate_skills.intersection(core_required))),
        "core_missing": sorted(list(core_required - candidate_skills)),
        "supporting_matched": sorted(list(candidate_skills.intersection(supporting_required))),
        "supporting_missing": sorted(list(supporting_required - candidate_skills)),
    }

def recommend_roles(resume_skills, skill_evidence_levels=None):
    results = [
        calculate_role_suitability(
            resume_skills,
            role_name,
            skill_evidence_levels=skill_evidence_levels
        )
        for role_name in ROLE_PROFILES
    ]

    results.sort(
        key=lambda x: (
            x["coverage"],
            len(x.get("matched_skills", [])),
            -len(x.get("missing_skills", [])),
            x["role"]
        ),
        reverse=True
    )

    return results