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
        extract_resume_sections,
        find_contextual_skill_evidence,
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
        extract_resume_sections,
        find_contextual_skill_evidence,
    )
    from bert_category_predictor import predict_top_categories
    from recommendations import generate_recommendations
    from capability_engine import analyze_capabilities


def calculate_skill_score(
    matched_skills,
    required_skills,
    skill_evidence_levels=None
):
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

    return (
        semantic_score * semantic_weight
        + skill_score * skill_weight
    )


RESPONSIBILITY_PATTERNS = [
    {
        "name": "api development",
        "patterns": [
            "api development",
            "restful or graphql apis",
            "scalable restful or graphql apis",
            "restful apis",
            "graphql apis",
            "rest apis",
            "api endpoints"
        ],
        "related_skills": [
            "rest api",
            "graphql",
            "node.js",
            "fastapi",
            "flask",
            "spring boot"
        ]
    },
    {
        "name": "system architecture and db schemas",
        "patterns": [
            "architecture & system design",
            "architect clean, maintainable server-side code",
            "server-side code and define database schemas",
            "database schemas for optimal data storage",
            "database schemas",
            "system architecture"
        ],
        "related_skills": [
            "java",
            "spring boot",
            "sql",
            "mysql",
            "postgresql",
            "database"
        ]
    },
    {
        "name": "performance tuning",
        "patterns": [
            "performance tuning",
            "optimize backend systems",
            "speed, scalability, and efficiency",
            "high traffic volume",
            "performance optimization"
        ],
        "related_skills": [
            "java",
            "sql",
            "python",
            "redis"
        ]
    },
    {
        "name": "security and compliance",
        "patterns": [
            "security & compliance",
            "user authentication",
            "oauth",
            "jwt",
            "secure authorization protocols",
            "data protection"
        ],
        "related_skills": [
            "rest api",
            "java",
            "spring boot",
            "node.js"
        ]
    },
    {
        "name": "testing and deployment",
        "patterns": [
            "testing & deployment",
            "unit and integration tests",
            "ci/cd pipeline deployments",
            "ci/cd pipeline",
            "debug software issues and support ci/cd"
        ],
        "related_skills": [
            "ci/cd",
            "git",
            "docker"
        ]
    },
    {
        "name": "predictive modeling and ml",
        "patterns": [
            "build predictive models",
            "predictive models and machine learning",
            "machine learning algorithms",
            "predictive modeling",
            "build predictive models and machine learning algorithms"
        ],
        "related_skills": [
            "machine learning",
            "predictive modeling",
            "scikit-learn",
            "deep learning",
            "python"
        ]
    },
    {
        "name": "data cleaning and aggregation",
        "patterns": [
            "clean, aggregate, and analyze data",
            "disparate sources",
            "clean and aggregate",
            "data cleaning and preprocessing"
        ],
        "related_skills": [
            "data cleaning",
            "data analysis",
            "sql",
            "python",
            "excel"
        ]
    },
    {
        "name": "business insights and kpis",
        "patterns": [
            "present data-driven insights",
            "strategic recommendations to stakeholders",
            "insights and strategic recommendations",
            "kpi metrics",
            "business stakeholders"
        ],
        "related_skills": [
            "kpi",
            "data analysis",
            "power bi",
            "excel",
            "tableau"
        ]
    },
    {
        "name": "ui ux design collaboration",
        "patterns": [
            "collaborate with designers",
            "translate wireframes",
            "wireframes into intuitive user experiences",
            "design systems"
        ],
        "related_skills": [
            "ui/ux",
            "figma",
            "adobe xd",
            "css",
            "html"
        ]
    },
    {
        "name": "dashboard development",
        "patterns": [
            "interactive dashboards",
            "dashboards and reports",
            "dashboards to track",
            "power bi dashboards"
        ],
        "related_skills": [
            "power bi",
            "tableau",
            "excel",
            "dashboard",
            "data visualization"
        ]
    },
    {
        "name": "sql data querying",
        "patterns": [
            "query relational databases",
            "relational databases using sql",
            "using sql to extract",
            "querying"
        ],
        "related_skills": [
            "sql",
            "mysql",
            "database"
        ]
    },
    {
        "name": "version control",
        "patterns": [
            "git and github",
            "git/github",
            "version control",
            "collaborative development",
            "git workflows"
        ],
        "related_skills": [
            "git",
            "github"
        ]
    }
]


def extract_job_responsibilities(job_description):
    text = str(job_description or "").replace("\r", "\n")
    responsibilities = []
    in_responsibilities = False

    # STRICT STOPS: Never parse qualification headings, education, or core languages as responsibilities!
    section_stops = {
        "required qualifications & skills", "required qualifications and skills",
        "required qualifications", "key requirements", "qualifications",
        "requirements", "education", "education:", "core languages", "core languages:",
        "preferred skills", "nice to have"
    }

    lines = text.splitlines()
    for line in lines:
        raw_clean = line.strip()
        if not raw_clean:
            continue

        clean = raw_clean.lstrip("•-* \t")
        heading = re.sub(r"^[\s•\-*#●]+", "", raw_clean).rstrip(":").strip().lower()

        if heading in {
            "responsibilities", "responsibility", "job responsibilities", 
            "key responsibilities", "core responsibilities", "what you'll do", "what you will do"
        }:
            in_responsibilities = True
            continue

        if in_responsibilities:
            # Stop if we hit a new major section header
            if any(stop_heading in heading for stop_heading in section_stops):
                in_responsibilities = False
                break
            
            # Guard against lines formatted like 'Education: Bachelor's' or 'Core Languages: ...'
            if re.match(r"^(education|core languages|required qualifications|requirements):", heading):
                in_responsibilities = False
                break

            if len(clean) > 12:
                responsibilities.append(clean)

    if not responsibilities:
        action_verb_pattern = r"^(Build|Develop|Design|Implement|Manage|Lead|Collaborate|Create|Maintain|Query|Integrate|Optimize|Drive|Architect|Analyze|Conduct|Write|Clean|Present)\b"
        for line in lines:
            clean = line.strip().lstrip("•-* \t")
            if re.search(action_verb_pattern, clean, flags=re.I) and len(clean) > 20:
                responsibilities.append(clean)

    return responsibilities[:8]


def find_responsibility_rule(responsibility):
    normalized = normalize_text(responsibility)
    priority = [
        "api development",
        "system architecture and db schemas",
        "performance tuning",
        "security and compliance",
        "testing and deployment",
        "predictive modeling and ml",
        "data cleaning and aggregation",
        "dashboard development",
        "ui ux design collaboration",
        "sql data querying",
        "business insights and kpis",
        "version control"
    ]

    ordered_rules = sorted(
        RESPONSIBILITY_PATTERNS,
        key=lambda rule: priority.index(rule["name"]) if rule["name"] in priority else len(priority)
    )

    for rule in ordered_rules:
        for pattern in rule["patterns"]:
            if normalize_text(pattern) in normalized:
                return rule

    return None


def _build_substantive_resume_text(resume_text):
    text = str(resume_text or "").replace("\r", "\n")
    lines = text.splitlines()
    output = []
    in_skills = False

    skill_headings = {
        "skills", "technical skills", "technical skills & tools", "skills & tools", "core skills",
    }

    section_headings = {
        "education", "experience", "work experience", "internships", "projects",
        "project", "certifications", "certification", "achievements", "extracurricular",
        "profile", "summary", "objective", "languages", "hobbies",
    }

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        heading = re.sub(r"^[\s\-•*]+", "", line).rstrip(":").strip().lower()
        if heading in skill_headings:
            in_skills = True
            continue

        if in_skills and heading in section_headings:
            in_skills = False

        if in_skills or re.search(r"https?://|www\.|@", line, flags=re.I):
            continue

        output.append(line)

    return "\n".join(output)


def analyze_job_responsibilities(resume_text, job_description, skill_evidence_levels=None):
    responsibilities = extract_job_responsibilities(job_description)
    evidence_text = _build_substantive_resume_text(resume_text)
    normalized_resume = normalize_text(evidence_text)

    try:
        resume_skills = set(extract_skills(resume_text))
    except Exception:
        resume_skills = set()

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

        direct_patterns = []
        if rule["name"] == "api development":
            direct_patterns = ["rest api", "restful api", "rest apis", "restful apis", "api endpoints"]
        elif rule["name"] == "system architecture and db schemas":
            direct_patterns = ["server-side", "database schemas", "architect", "database management", "relational database"]
        elif rule["name"] == "predictive modeling and ml":
            direct_patterns = ["machine learning-based", "machine learning", "prediction and academic", "predictive modeling", "random forest"]
        elif rule["name"] == "data cleaning and aggregation":
            direct_patterns = ["analyzed large, multi-source datasets", "multi-source datasets using python and sql", "clean and aggregate"]
        elif rule["name"] == "business insights and kpis":
            direct_patterns = ["designed and built interactive power bi dashboards", "track key performance indicators", "support data-driven business decisions"]
        elif rule["name"] == "sql data querying":
            direct_patterns = ["datasets using python and sql", "query relational databases"]
        elif rule["name"] == "version control":
            direct_patterns = ["git version control", "git workflows"]

        raw_direct = []
        for pattern in direct_patterns:
            normalized_pattern = normalize_text(pattern)
            if normalized_pattern and normalized_pattern in normalized_resume:
                raw_direct.append(pattern)

        unique_direct = []
        for pat in sorted(raw_direct, key=len, reverse=True):
            if not any(pat in existing for existing in unique_direct):
                unique_direct.append(pat)

        direct_evidence = [{
            "evidence": pat,
            "source": "experience/project/education"
        } for pat in unique_direct]

        related_evidence = []
        for related_skill in rule["related_skills"]:
            if related_skill not in resume_skills:
                continue
            try:
                skill_evidence = find_contextual_skill_evidence(evidence_text, related_skill)
            except Exception:
                skill_evidence = []

            if skill_evidence:
                related_evidence.append({
                    "skill": related_skill,
                    "evidence": skill_evidence
                })

        if direct_evidence:
            status = "strong"
            reason = "The resume contains direct evidence in experience or projects supporting this responsibility."
        elif rule["name"] == "sql data querying" and ("sql" in resume_skills or "mysql" in resume_skills):
            status = "related"
            via_tool = "via MySQL" if "mysql" in resume_skills else "listed only"
            reason = f"SQL / Database ({via_tool}, no project querying context)"
            related_evidence.append({
                "skill": "sql",
                "evidence": [{"snippet": f"Identified in technical competencies ({via_tool})."}]
            })
        elif related_evidence:
            matched_names = ", ".join(format_skill_display(e["skill"]) for e in related_evidence)
            status = "related"
            reason = f"Supporting skills detected ({matched_names}), but lack dedicated project delivery context."
        else:
            status = "missing"
            reason = "No direct or meaningful related evidence was detected in the resume."

        results.append({
            "responsibility": responsibility,
            "status": status,
            "evidence": direct_evidence,
            "related_evidence": related_evidence,
            "reason": reason,
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