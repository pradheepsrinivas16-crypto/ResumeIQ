from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

CAPABILITIES = {
    "frontend development": {
        "description": "Ability to build user-facing web interfaces using HTML, CSS, JavaScript and modern frontend frameworks.",
        "core_skills": {"html", "css", "javascript"},
        "supporting_skills": {"react", "angular", "vue", "responsive web design", "ui/ux", "typescript"},
        "minimum_core": 2,
        "minimum_supporting": 1
    },
    "backend development": {
        "description": "Ability to develop server-side applications, backend services and application logic.",
        "core_skills": {"spring boot", "node.js", "fastapi", "flask", "django", "rest api"},
        "supporting_skills": {"java", "sql", "mysql", "postgresql", "python"},
        "minimum_core": 1,
        "minimum_supporting": 1
    },
    "full stack development": {
        "description": "Ability to combine frontend and backend development to build complete web applications.",
        "core_skills": {"html", "css", "javascript"},
        "backend_core": {"spring boot", "node.js", "fastapi", "flask", "django", "rest api"},
        "supporting_skills": {"react", "angular", "java", "mysql", "sql", "postgresql"},
        "minimum_core": 2,
        "minimum_supporting": 1
    },
    "database development": {
        "description": "Ability to work with relational databases and database-driven applications.",
        "core_skills": {"sql", "mysql", "postgresql"},
        "supporting_skills": {"crud", "mongodb", "database", "database management", "redis"},
        "minimum_core": 1,
        "minimum_supporting": 1
    },
    "api development": {
        "description": "Ability to design or integrate application programming interfaces and backend services.",
        "core_skills": {"rest api", "graphql"},
        "supporting_skills": {"java", "spring boot", "node.js", "javascript", "fastapi"},
        "minimum_core": 1,
        "minimum_supporting": 1
    },
    "ui ux development": {
        "description": "Ability to design usable and visually effective interfaces using UI/UX principles and design tools.",
        "core_skills": {"figma", "ui/ux", "adobe xd"},
        "supporting_skills": {"responsive web design", "html", "css", "javascript", "canva"},
        "minimum_core": 1,
        "minimum_supporting": 1
    },
    "cloud development": {
        "description": "Ability to work with cloud platforms and cloud-based application infrastructure.",
        "core_skills": {"aws", "azure", "google cloud", "gcp"},
        "supporting_skills": {"docker", "kubernetes", "cloud", "cloud computing"},
        "minimum_core": 1,
        "minimum_supporting": 1
    },
    "version control": {
        "description": "Ability to manage source code and collaborate using version-control platforms.",
        "core_skills": {"git", "github"},
        "supporting_skills": {"gitlab", "bitbucket", "version control"},
        "minimum_core": 1,
        "minimum_supporting": 0
    },
    "data science": {
        "description": "Ability to work with data using programming, data analysis, statistics and machine learning.",
        "core_skills": {"python", "machine learning", "statistical analysis"},
        "supporting_skills": {"pandas", "numpy", "scikit-learn", "data analysis", "predictive modeling"},
        "minimum_core": 2,
        "minimum_supporting": 1
    },
    "data analytics": {
        "description": "Ability to analyze data, identify trends and communicate insights using analytical tools.",
        "core_skills": {"data analysis", "sql", "data visualization"},
        "supporting_skills": {"excel", "power bi", "tableau", "dashboard", "statistical analysis", "data cleaning", "exploratory data analysis"},
        "minimum_core": 2,
        "minimum_supporting": 1
    },
    "machine learning": {
        "description": "Ability to develop predictive models using machine learning algorithms and data.",
        "core_skills": {"machine learning", "scikit-learn", "deep learning", "predictive modeling"},
        "supporting_skills": {"python", "pandas", "numpy", "tensorflow", "pytorch", "data analysis"},
        "minimum_core": 1,
        "minimum_supporting": 2
    },
    "business intelligence": {
        "description": "Ability to transform business data into dashboards, reports and actionable insights.",
        "core_skills": {"power bi", "tableau", "dashboard"},
        "supporting_skills": {"sql", "excel", "data visualization", "kpi", "data analysis"},
        "minimum_core": 1,
        "minimum_supporting": 2
    },
    "data visualization": {
        "description": "Ability to communicate information through charts, dashboards and visual representations.",
        "core_skills": {"data visualization", "power bi", "tableau"},
        "supporting_skills": {"matplotlib", "seaborn", "dashboard", "excel"},
        "minimum_core": 1,
        "minimum_supporting": 1
    }
}

def normalize_skills(skills):
    if not skills:
        return set()
    return {str(skill).lower().strip() for skill in skills if str(skill).strip()}

def analyze_job_relevant_capabilities(resume_skills, job_skills, skill_evidence_levels=None):
    resume_skills = normalize_skills(resume_skills)
    job_skills = normalize_skills(job_skills)
    evidence_levels = skill_evidence_levels or {}

    if not job_skills:
        return []

    if any(g in resume_skills for g in ["git", "github", "gitlab"]):
        resume_skills.add("git")
        resume_skills.add("version control")

    results = []

    for capability_name, capability in CAPABILITIES.items():
        core_skills = set(capability.get("core_skills", set()))
        supporting_skills = set(capability.get("supporting_skills", set()))
        backend_core = set(capability.get("backend_core", set()))
        capability_skills = core_skills | supporting_skills | backend_core

        relevant_job_skills = sorted(job_skills.intersection(capability_skills))
        if not relevant_job_skills:
            continue

        matched = []
        earned_weight = 0.0

        for s in relevant_job_skills:
            is_matched = False
            sub_label = None

            if s in resume_skills:
                is_matched = True
            elif s in {"git", "version control"} and any(g in resume_skills for g in ["git", "github", "gitlab", "version control"]):
                is_matched = True
            elif s == "adobe xd" and "figma" in resume_skills:
                is_matched = True
                sub_label = "Adobe Xd (Sub: Figma)"
            elif s == "power bi" and "tableau" in resume_skills:
                is_matched = True
                sub_label = "Power BI (Sub: Tableau)"
            elif s == "mysql" and "postgresql" in resume_skills:
                is_matched = True
                sub_label = "MySQL (Sub: PostgreSQL)"

            if is_matched:
                matched.append(sub_label if sub_label else s)
                status = str(evidence_levels.get(s, {}).get("status", "demonstrated")).strip().lower()
                if "listed" in status:
                    earned_weight += 0.40
                elif "supporting" in status or "substitute" in status:
                    earned_weight += 0.70
                else:
                    earned_weight += 1.00

        matched = sorted(list(set(matched)))
        missing = []
        for s in relevant_job_skills:
            if not any(s == m or str(m).lower().startswith(f"{s} (sub:") for m in matched):
                missing.append(s)
        missing = sorted(list(set(missing)))

        # Tier-weighted evidence coverage
        coverage = (earned_weight / len(relevant_job_skills) * 100) if relevant_job_skills else 0.0

        # Strict Gating Rules to prevent overclaiming
        has_fullstack_core = bool(resume_skills.intersection(core_skills)) and bool(resume_skills.intersection(backend_core))
        has_ml_core = bool(resume_skills.intersection({"machine learning", "scikit-learn", "deep learning", "predictive modeling"}))
        has_backend_core = bool(resume_skills.intersection(core_skills))

        if capability_name == "full stack development" and not has_fullstack_core:
            alignment = "Low Alignment"
            coverage = min(coverage, 35.0)
        elif capability_name in {"machine learning", "data science"} and not has_ml_core:
            alignment = "Low Alignment"
            coverage = min(coverage, 40.0)
        elif capability_name == "backend development" and not has_backend_core:
            alignment = "Low Alignment"
            coverage = min(coverage, 35.0)
        else:
            if coverage >= 85.0:
                alignment = "Strong Alignment"
            elif coverage >= 45.0:
                alignment = "Partial Alignment"
            else:
                alignment = "Low Alignment"

        requirement_type = (
            "Required"
            if relevant_job_skills and set(relevant_job_skills).intersection(core_skills)
            else "Supporting"
        )

        results.append({
            "capability": capability_name,
            "description": capability["description"],
            "relevant_job_skills": relevant_job_skills,
            "matched_skills": matched,
            "missing_skills": missing,
            "coverage": coverage,
            "alignment": alignment,
            "requirement_type": requirement_type
        })

    results.sort(
        key=lambda item: (
            item["coverage"],
            len(item["relevant_job_skills"]),
            1 if item["requirement_type"] == "Required" else 0
        ),
        reverse=True
    )
    return results

def analyze_capabilities(resume_skills):
    resume_skills = normalize_skills(resume_skills)
    results = []
    for capability_name, capability in CAPABILITIES.items():
        core = set(capability.get("core_skills", set()))
        supp = set(capability.get("supporting_skills", set()))
        core_m = sorted(resume_skills.intersection(core))
        supp_m = sorted(resume_skills.intersection(supp))
        supported = (len(core_m) >= capability.get("minimum_core", 1)) and (len(supp_m) >= capability.get("minimum_supporting", 0))

        if capability_name == "full stack development":
            backend_core = set(capability.get("backend_core", set()))
            supported = supported and bool(resume_skills.intersection(core)) and bool(resume_skills.intersection(backend_core))

        if capability_name in {"machine learning", "data science"}:
            supported = supported and bool(resume_skills.intersection({"machine learning", "scikit-learn", "deep learning", "predictive modeling"}))

        results.append({
            "capability": capability_name,
            "description": capability["description"],
            "supported": supported,
            "core_matches": core_m,
            "supporting_matches": supp_m,
            "evidence_count": len(core_m) + len(supp_m)
        })
    return results