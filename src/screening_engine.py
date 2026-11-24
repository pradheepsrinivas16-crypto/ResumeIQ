import os
import sys
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
for p in [CURRENT_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from src.job_matcher import calculate_match_score
    from src.skill_matcher import (
        compare_skills,
        extract_skills,
        normalize_text,
        classify_skill_evidence,
        format_skill_display,
    )
    from src.bert_category_predictor import predict_top_categories
    from src.recommendations import generate_recommendations
    from src.capability_engine import analyze_capabilities
except ImportError:
    from job_matcher import calculate_match_score
    from skill_matcher import (
        compare_skills,
        extract_skills,
        normalize_text,
        classify_skill_evidence,
        format_skill_display,
    )
    from bert_category_predictor import predict_top_categories
    from recommendations import generate_recommendations
    from capability_engine import analyze_capabilities


def calculate_skill_score(matched_skills, required_skills, skill_evidence_levels=None):
    if not required_skills:
        return 0.0

    skill_evidence_levels = skill_evidence_levels or {}
    evidence_weights = {
        "demonstrated": 1.00,
        "substitute": 0.75,
        "supporting": 0.70,
        "listed": 0.40,
        "listed_only": 0.40,
        "missing": 0.00,
    }

    total_score = 0.0
    for skill in required_skills:
        evidence = skill_evidence_levels.get(skill, {})
        status = str(evidence.get("status", "missing")).strip().lower()
        total_score += evidence_weights.get(status, 0.00)

    return (total_score / len(required_skills)) * 100


def calculate_final_score(
    semantic_score,
    skill_score,
    skill_score_available=True,
    semantic_weight=0.60,
    skill_weight=0.40
):
    if not skill_score_available:
        return semantic_score
    return (semantic_score * semantic_weight + skill_score * skill_weight)


RESPONSIBILITY_PATTERNS = [
    {
        "name": "responsive web development",
        "patterns": [
            "develop responsive web applications",
            "responsive web applications",
            "responsive web development",
            "html, css, and javascript"
        ],
        "related_skills": ["responsive web design", "html", "css", "javascript"]
    },
    {
        "name": "frontend framework development",
        "patterns": [
            "build modular ui components",
            "modern frontend frameworks",
            "react or angular",
            "interactive frontend applications"
        ],
        "related_skills": ["react", "angular"]
    },
    {
        "name": "ui ux design collaboration",
        "patterns": [
            "collaborate with designers",
            "translate figma",
            "adobe xd wireframes",
            "intuitive user experiences"
        ],
        "related_skills": ["figma", "adobe xd", "ui/ux"]
    },
    {
        "name": "api integration and version control",
        "patterns": [
            "integrate frontend applications with backend rest apis",
            "manage source code using git",
            "backend rest apis"
        ],
        "related_skills": ["rest api", "git"]
    },
    {
        "name": "api development",
        "patterns": [
            "restful or graphql apis",
            "scalable restful or graphql apis",
            "restful apis",
            "graphql apis",
            "rest apis"
        ],
        "related_skills": ["rest api", "graphql", "node.js", "fastapi", "flask", "spring boot"]
    },
    {
        "name": "system architecture and db schemas",
        "patterns": [
            "architect clean, maintainable server-side code",
            "define database schemas",
            "database schemas for optimal data storage"
        ],
        "related_skills": ["spring boot", "django", "fastapi", "node.js", "rest api"]
    },
    {
        "name": "performance tuning",
        "patterns": [
            "optimize backend systems",
            "speed, scalability, and efficiency",
            "high traffic volume"
        ],
        "related_skills": ["java", "sql", "python", "redis"]
    },
    {
        "name": "security and compliance",
        "patterns": [
            "user authentication",
            "oauth",
            "jwt",
            "secure authorization protocols",
            "data protection"
        ],
        "related_skills": ["rest api", "java", "spring boot", "node.js"]
    },
    {
        "name": "testing and deployment",
        "patterns": [
            "unit and integration tests",
            "ci/cd pipeline deployments",
            "debug software issues and support ci/cd"
        ],
        "related_skills": ["ci/cd", "docker", "jenkins", "github actions"]
    },
    {
        "name": "predictive modeling and ml",
        "patterns": [
            "build predictive models",
            "predictive models and machine learning",
            "machine learning algorithms"
        ],
        "related_skills": ["machine learning", "predictive modeling", "scikit-learn", "deep learning", "python"]
    },
    {
        "name": "data cleaning and aggregation",
        "patterns": [
            "clean, aggregate, and analyze data",
            "disparate sources",
            "clean and aggregate"
        ],
        "related_skills": ["data cleaning", "data analysis", "sql", "python", "excel"]
    },
    {
        "name": "business insights and kpis",
        "patterns": [
            "present data-driven insights",
            "strategic recommendations to stakeholders",
            "kpi metrics"
        ],
        "related_skills": ["kpi", "data analysis", "power bi", "excel", "tableau"]
    },
    {
        "name": "dashboard development",
        "patterns": [
            "interactive dashboards",
            "dashboards and reports",
            "power bi and excel"
        ],
        "related_skills": ["power bi", "tableau", "excel", "dashboard", "data visualization"]
    },
    {
        "name": "sql data querying",
        "patterns": [
            "query relational databases",
            "relational databases using sql",
            "using sql to extract"
        ],
        "related_skills": ["sql", "mysql", "database"]
    },
    {
        "name": "exploratory data analysis",
        "patterns": [
            "exploratory data analysis",
            "statistical modeling",
            "pandas and numpy"
        ],
        "related_skills": ["exploratory data analysis", "statistical analysis", "pandas", "numpy", "python"]
    },
    {
        "name": "git version control workflows",
        "patterns": [
            "collaborate using git",
            "git version control workflows",
            "version control workflows"
        ],
        "related_skills": ["git", "github", "gitlab"]
    },
]


def extract_job_responsibilities(job_description):
    """Extracts ONLY duty bullets under 'Responsibilities', halting before 'Required Skills'."""
    text = str(job_description or "").replace("\r", "\n")
    responsibilities = []
    in_responsibilities = False

    section_stops = {
        "required skills", "required skill", "required qualifications",
        "required qualifications & skills", "key requirements", "qualifications",
        "requirements", "education", "core languages", "preferred skills", "nice to have"
    }

    lines = text.splitlines()
    for line in lines:
        raw_clean = line.strip()
        if not raw_clean:
            continue

        heading = re.sub(r"^[\s•\-*#●]+", "", raw_clean).rstrip(":").strip().lower()

        if heading in {
            "responsibilities", "responsibility", "job responsibilities",
            "key responsibilities", "core responsibilities", "what you'll do", "what you will do"
        }:
            in_responsibilities = True
            continue

        if in_responsibilities:
            if heading in section_stops or any(heading.startswith(s) for s in section_stops):
                break
            clean_bullet = raw_clean.lstrip("•-* \t").strip()
            if len(clean_bullet) > 12:
                responsibilities.append(clean_bullet)

    return responsibilities[:8]


def find_responsibility_rule(responsibility):
    normalized = normalize_text(responsibility)
    for rule in RESPONSIBILITY_PATTERNS:
        for pattern in rule["patterns"]:
            if normalize_text(pattern) in normalized:
                return rule
    return None


def analyze_job_responsibilities(resume_text, job_description, skill_evidence_levels=None):
    responsibilities = extract_job_responsibilities(job_description)
    results = []

    for responsibility in responsibilities:
        rule = find_responsibility_rule(responsibility)
        if rule is None:
            results.append({
                "responsibility": responsibility,
                "status": "missing",
                "evidence": [],
                "related_evidence": [],
                "reason": "No direct or meaningful related evidence was detected in the resume."
            })
            continue

        matched_tiers = []
        for sk in rule["related_skills"]:
            ev = classify_skill_evidence(resume_text, sk)
            st = ev.get("status", "missing")
            if st != "missing":
                matched_tiers.append((sk, st, ev.get("snippet", "")))

        if not matched_tiers:
            results.append({
                "responsibility": responsibility,
                "status": "missing",
                "evidence": [],
                "related_evidence": [],
                "reason": "No direct or meaningful related evidence was detected in the resume."
            })
            continue

        has_demonstrated = any(t[1] == "demonstrated" for t in matched_tiers)
        has_supporting = any(t[1] in {"supporting", "substitute"} for t in matched_tiers)

        if has_demonstrated:
            dem_items = [t for t in matched_tiers if t[1] == "demonstrated"]
            results.append({
                "responsibility": responsibility,
                "status": "strong",
                "evidence": [{"evidence": t[2] or format_skill_display(t[0])} for t in dem_items],
                "related_evidence": [],
                "reason": "Verified in active work or project sentences."
            })
        elif has_supporting:
            supp_items = [t for t in matched_tiers if t[1] in {"supporting", "substitute"}]
            results.append({
                "responsibility": responsibility,
                "status": "related",
                "evidence": [],
                "related_evidence": [{"skill": format_skill_display(t[0]), "tier_label": "supporting"} for t in supp_items],
                "reason": f"Supporting context detected ({', '.join(format_skill_display(t[0]) for t in supp_items)})."
            })
        else:
            list_items = [t for t in matched_tiers if t[1] == "listed"]
            raw_names = [t[0] for t in list_items]
            if "mysql" in raw_names:
                list_items = [t for t in list_items if t[0] == "mysql"]
            elif "postgresql" in raw_names:
                list_items = [t for t in list_items if t[0] == "postgresql"]

            results.append({
                "responsibility": responsibility,
                "status": "related",
                "evidence": [],
                "related_evidence": [{"skill": f"{format_skill_display(t[0])} (listed only)", "tier_label": "listed only"} for t in list_items],
                "reason": f"Matched in technical skills list only ({', '.join(format_skill_display(t[0]) for t in list_items)})."
            })

    summary = {
        "strong": sum(r["status"] == "strong" for r in results),
        "related": sum(r["status"] == "related" for r in results),
        "missing": sum(r["status"] == "missing" for r in results),
        "unknown": sum(r["status"] == "unknown" for r in results),
    }

    return {
        "responsibilities": results,
        "summary": summary,
    }


def get_fit_tier_and_divergence(final_score, semantic_score, skill_score):
    divergence = round(semantic_score - skill_score, 1)
    has_divergence_warning = divergence > 30.0
    divergence_msg = (
        f"High semantic similarity ({semantic_score:.1f}%) but low verified skill evidence ({skill_score:.1f}%) — review manually."
        if has_divergence_warning else ""
    )

    if final_score >= 75.0 and skill_score >= 60.0:
        fit_label = "Strong Fit"
    elif final_score >= 50.0 and skill_score >= 40.0:
        fit_label = "Moderate Fit"
    elif final_score >= 50.0 and skill_score < 40.0:
        fit_label = "Low Evidence"
    else:
        fit_label = "Low Fit"

    return fit_label, has_divergence_warning, divergence_msg


def screen_resume(resume_text, job_description):
    semantic_score = calculate_match_score(resume_text, job_description)
    skill_result = compare_skills(resume_text, job_description)

    required_skills = skill_result["required_skills"]
    skill_score_available = bool(required_skills)

    ssot_evidence_levels = skill_result.get(
        "required_skill_evidence_levels",
        skill_result.get("skill_evidence_levels", {})
    )

    skill_score = calculate_skill_score(
        skill_result["matched_skills"],
        required_skills,
        ssot_evidence_levels
    )

    final_score = calculate_final_score(
        semantic_score,
        skill_score,
        skill_score_available
    )

    fit_label, has_divergence_warning, divergence_msg = get_fit_tier_and_divergence(
        final_score, semantic_score, skill_score
    )

    bert_categories = predict_top_categories(resume_text, top_k=3)
    category = bert_categories[0]["category"] if bert_categories else "Unknown"
    category_confidence = bert_categories[0]["confidence"] if bert_categories else 0.0

    recommendations = generate_recommendations(
        skill_result["matched_skills"],
        skill_result["missing_skills"],
        semantic_score,
        skill_score,
        required_skills,
        skill_evidence_levels=ssot_evidence_levels
    )

    capability_results = analyze_capabilities(skill_result["resume_skills"])
    responsibility_analysis = analyze_job_responsibilities(
        resume_text,
        job_description,
        skill_evidence_levels=ssot_evidence_levels
    )

    return {
        "final_score": final_score,
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "skill_score_available": skill_score_available,
        "fit_label": fit_label,
        "has_divergence_warning": has_divergence_warning,
        "divergence_warning": divergence_msg,
        "category": category,
        "category_confidence": category_confidence,
        "bert_categories": bert_categories,
        "required_skills": required_skills,
        "matched_skills": skill_result["matched_skills"],
        "related_skills": skill_result.get("related_skills", []),
        "missing_skills": skill_result["missing_skills"],
        "skill_evidence": skill_result.get("skill_evidence", {}),
        "skill_evidence_levels": skill_result.get("skill_evidence_levels", {}),
        "required_skill_evidence_levels": ssot_evidence_levels,
        "preferred_skills": skill_result.get("preferred_skills", []),
        "preferred_matched_skills": skill_result.get("preferred_matched_skills", []),
        "preferred_related_skills": skill_result.get("preferred_related_skills", []),
        "preferred_missing_skills": skill_result.get("preferred_missing_skills", []),
        "preferred_skill_evidence": skill_result.get("preferred_skill_evidence", {}),
        "candidate_strengths": skill_result.get("candidate_strengths", []),
        "candidate_related": skill_result.get("candidate_related", []),
        "candidate_gaps": skill_result.get("candidate_gaps", []),
        "resume_skills": skill_result["resume_skills"],
        "strengths": recommendations["strengths"],
        "skill_gaps": recommendations["skill_gaps"],
        "suggestions": recommendations["suggestions"],
        "score_explanation": recommendations.get("score_explanation", []),
        "capabilities": capability_results,
        "responsibility_analysis": responsibility_analysis,
    }