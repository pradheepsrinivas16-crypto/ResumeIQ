import re


# ============================================================
# SCREENING ENGINE
# ============================================================

from .job_matcher import calculate_match_score
from .skill_matcher import (
    compare_skills,
    extract_skills,
    normalize_text,
    extract_resume_sections,
    find_contextual_skill_evidence,
)
from .bert_category_predictor import predict_top_categories
from .recommendations import generate_recommendations
from .capability_engine import analyze_capabilities


# ============================================================
# SKILL SCORE
# ============================================================


def calculate_skill_score(
    matched_skills,
    required_skills,
    skill_evidence_levels=None
):
    """
    Calculate evidence-aware required-skill coverage.

    Evidence strength:

        Demonstrated -> 1.00
        Supporting   -> 0.70
        Listed Only  -> 0.40
        Missing      -> 0.00

    This prevents a skill mentioned only in the Skills section
    from receiving the same weight as a skill demonstrated through
    actual project or work experience.
    """

    if not required_skills:
        return 0.0

    skill_evidence_levels = skill_evidence_levels or {}

    evidence_weights = {
        "demonstrated": 1.00,
        "substitute": 0.75,  # Valid industry equivalent tool (e.g. Figma for Adobe XD)
        "supporting": 0.70,
        "listed": 0.40,
        "listed_only": 0.40,
        "missing": 0.00,
    }

    total_score = 0.0

    for skill in required_skills:

        evidence = skill_evidence_levels.get(
            skill,
            {}
        )

        status = str(
            evidence.get(
                "status",
                "missing"
            )
        ).strip().lower()

        total_score += evidence_weights.get(
            status,
            0.00
        )

    return (
        total_score / len(required_skills)
    ) * 100


# ============================================================
# FINAL SCORE
# ============================================================


def calculate_final_score(
    semantic_score,
    skill_score,
    skill_score_available=True,
    semantic_weight=0.60,
    skill_weight=0.40
):
    """
    Calculate final compatibility score.

    If no recognized required skills exist,
    semantic compatibility is used directly.
    """

    if not skill_score_available:
        return semantic_score

    return (
        semantic_score * semantic_weight
        + skill_score * skill_weight
    )


# ============================================================
# JOB RESPONSIBILITY ANALYSIS
# ============================================================


RESPONSIBILITY_PATTERNS = [

    {
        "name": "responsive web development",

        "patterns": [
            "responsive web applications",
            "responsive web application",
            "responsive web development",
            "responsive design",
        ],

        "related_skills": [
            "html",
            "css",
            "javascript",
            "responsive web design",
        ],
    },

    {
        "name": "react frontend development",

        "patterns": [
            "interactive frontend applications using react",
            "frontend applications using react",
            "react frontend",
            "frontend development using react",
            "react applications",
        ],

        "related_skills": [
            "react",
            "javascript",
            "html",
            "css",
        ],
    },

    {
        "name": "backend development",

        "patterns": [
            "backend services",
            "backend development",
            "backend applications",
            "server-side",
            "server side",
        ],

        "related_skills": [
            "java",
            "spring boot",
            "node.js",
            "rest api",
        ],
    },

    {
        "name": "rest api development",

        "patterns": [
            "rest apis",
            "rest api",
            "restful apis",
            "restful api",
            "api development",
        ],

        "related_skills": [
            "java",
            "spring boot",
            "node.js",
        ],
    },

    {
        "name": "database development",

        "patterns": [
            "relational databases",
            "database-driven applications",
            "database driven applications",
            "work with databases",
            "database applications",
        ],

        "related_skills": [
            "mysql",
        ],
    },

    {
        "name": "crud operations",

        "patterns": [
            "crud operations",
            "crud operation",
            "create read update delete",
        ],

        "related_skills": [
            "mysql",
        ],
    },

    {
        "name": "frontend backend integration",

        "patterns": [
            "integrate frontend applications with backend services",
            "frontend applications with backend services",
            "frontend with backend",
            "frontend-backend integration",
            "frontend backend integration",
        ],

        "related_skills": [
            "react",
            "java",
            "spring boot",
            "rest api",
            "javascript",
        ],
    },

    {
        "name": "testing and debugging",

        "patterns": [
            "debug, test",
            "debug and test",
            "debugging",
        ],

        "related_skills": [],
    },

    {
        "name": "software development best practices",

        "patterns": [
            "software development best practices",
            "software development best practice",
            "coding standards",
            "clean code",
            "software development lifecycle",
            "software development life cycle",
            "sdlc",
            "agile development",
            "agile methodology",
            "development best practices",
        ],

        "related_skills": [],
    },

    {
        "name": "testing web applications",

        "patterns": [
            "test web applications",
            "test and maintain",
            "debug",
        ],

        "related_skills": [],
    },

    {
        "name": "version control",

        "patterns": [
            "git and github",
            "git/github",
            "version control",
            "collaborative development",
        ],

        "related_skills": [
            "git",
            "github",
        ],
    },

    {
        "name": "scalable application development",

        "patterns": [
            "scalable applications",
            "scalable web applications",
            "scalable application",
        ],

        "related_skills": [],
    },

]


# ============================================================
# JOB RESPONSIBILITY EXTRACTION
# ============================================================


def extract_job_responsibilities(job_description):
    """
    Extract only the responsibilities from the explicit
    Responsibilities section of the JD.
    """

    text = str(
        job_description or ""
    ).replace(
        "\r",
        "\n"
    )

    responsibilities = []

    in_responsibilities = False

    section_stops = {
        "required skills",
        "required skill",
        "preferred skills",
        "preferred skill",
        "qualifications",
        "experience",
        "education",
        "requirements",
        "nice to have",
    }

    for line in text.splitlines():

        clean = line.strip()

        clean = clean.lstrip(
            "•-* \t"
        )

        if not clean:
            continue

        heading = clean.rstrip(
            ":"
        ).strip().lower()

        if heading in {
            "responsibilities",
            "responsibility",
            "job responsibilities",
        }:

            in_responsibilities = True

            continue

        if (
            in_responsibilities
            and heading in section_stops
        ):

            in_responsibilities = False

            continue

        if in_responsibilities:
            responsibilities.append(
                clean
            )

    return responsibilities


# ============================================================
# RESPONSIBILITY RULE
# ============================================================


def find_responsibility_rule(
    responsibility
):
    """
    Find the safest responsibility rule
    for one JD line.
    """

    normalized = normalize_text(
        responsibility
    )

    priority = [
        "crud operations",
        "rest api development",
        "version control",
        "testing and debugging",
        "frontend backend integration",
        "responsive web development",
        "react frontend development",
        "backend development",
        "database development",
        "software development best practices",
        "scalable application development",
    ]

    ordered_rules = sorted(
        RESPONSIBILITY_PATTERNS,
        key=lambda rule:
            priority.index(
                rule["name"]
            )
            if rule["name"] in priority
            else len(priority)
    )

    for rule in ordered_rules:

        for pattern in rule["patterns"]:

            if normalize_text(
                pattern
            ) in normalized:

                return rule

    return None


# ============================================================
# SUBSTANTIVE RESUME TEXT
# ============================================================


def _build_substantive_resume_text(
    resume_text
):
    """
    Build resume evidence while excluding
    contact and skills-only text.
    """

    text = str(
        resume_text or ""
    ).replace(
        "\r",
        "\n"
    )

    lines = text.splitlines()

    output = []

    in_skills = False

    skill_headings = {
        "skills",
        "technical skills",
        "technical skills & tools",
        "skills & tools",
        "core skills",
    }

    section_headings = {
        "education",
        "experience",
        "work experience",
        "internships",
        "projects",
        "project",
        "certifications",
        "certification",
        "achievements",
        "extracurricular",
        "profile",
        "summary",
        "objective",
        "languages",
        "hobbies",
    }

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        heading = re.sub(
            r"^[\s\-•*]+",
            "",
            line
        ).rstrip(
            ":"
        ).strip().lower()

        if heading in skill_headings:

            in_skills = True

            continue

        if (
            in_skills
            and heading in section_headings
        ):

            in_skills = False

        if in_skills:
            continue

        if re.search(
            r"https?://|www\.|@",
            line,
            flags=re.I
        ):
            continue

        output.append(line)

    return "\n".join(
        output
    )


# ============================================================
# JOB RESPONSIBILITY ANALYSIS
# ============================================================


def analyze_job_responsibilities(
    resume_text,
    job_description
):

    # EXPERIENCE-FIRST RESPONSIBILITY MATCHING
    #
    # A skill listed under a Skills section is not proof
    # that the candidate performed the corresponding
    # job responsibility.

    resume_sections = extract_resume_sections(
        resume_text
    )

    substantive_sections = {
        key: value
        for key, value in resume_sections.items()
        if key.lower()
        not in {
            "skills",
            "technical skills",
            "skills & technologies",
        }
    }

    responsibility_resume_text = "\n".join(
        substantive_sections.values()
    )

    responsibilities = extract_job_responsibilities(
        job_description
    )

    evidence_text = _build_substantive_resume_text(
        resume_text
    )

    normalized_resume = normalize_text(
        evidence_text
    )

    try:

        resume_skills = set(
            extract_skills(
                resume_text
            )
        )

    except Exception:

        resume_skills = set()

    results = []

    for responsibility in responsibilities:

        rule = find_responsibility_rule(
            responsibility
        )

        if rule is None:

            results.append({
                "responsibility": responsibility,
                "status": "unknown",
                "evidence": [],
                "related_evidence": [],
                "reason":
                    "No safe responsibility rule is available "
                    "for this requirement."
            })

            continue

        direct_patterns = []

        if rule["name"] == "responsive web development":

            direct_patterns = [
                "responsive",
                "responsive web",
                "responsive e-commerce",
                "responsive ecommerce",
            ]

        elif rule["name"] == "react frontend development":

            direct_patterns = [
                "react js",
                "reactjs",
                "react application",
                "react frontend",
                "react project",
                "react applications",
            ]

        elif rule["name"] == "backend development":

            direct_patterns = [
                "backend development",
                "backend services",
                "backend application",
                "server-side development",
                "server side development",
            ]

        elif rule["name"] == "rest api development":

            direct_patterns = [
                "rest api",
                "rest apis",
                "restful api",
                "restful apis",
                "api development",
                "api integration",
            ]

        elif rule["name"] == "database development":

            direct_patterns = [
                "database-driven",
                "database driven",
                "database management",
                "database application",
                "relational database",
            ]

        elif rule["name"] == "crud operations":

            direct_patterns = [
                "crud operations",
                "crud operation",
                "crud",
                "create read update delete",
            ]

        elif rule["name"] == "frontend backend integration":

            direct_patterns = [
                "frontend-backend",
                "frontend backend",
                "frontend with backend",
                "integrate frontend",
                "backend integration",
                "api integration",
            ]

        elif rule["name"] == "testing and debugging":

            direct_patterns = [
                "debugging",
                "debug",
                "testing web applications",
                "test web applications",
                "test and maintain",
                "tested",
            ]

        elif rule["name"] == "version control":

            # A Git/GitHub skill-list entry is not enough
            # to prove version-control responsibility.

            direct_patterns = [
                "git",
                "github",
                "version control",
            ]

        elif rule["name"] == "scalable application development":

            direct_patterns = [
                "scalable application",
                "scalable applications",
                "scalable web application",
                "scalable web applications",
                "scalable system",
                "scalable systems",
                "highly scalable",
                "scalability",
            ]

        direct_evidence = []

        related_evidence = []

        for pattern in direct_patterns:

            normalized_pattern = normalize_text(
                pattern
            )

            if (
                normalized_pattern
                and normalized_pattern
                in normalized_resume
            ):

                direct_evidence.append({
                    "evidence": pattern,
                    "source":
                        "experience/project/education"
                })

        for related_skill in rule[
            "related_skills"
        ]:

            if related_skill not in resume_skills:
                continue

            try:

                skill_evidence = (
                    find_contextual_skill_evidence(
                        evidence_text,
                        related_skill
                    )
                )

            except Exception:

                skill_evidence = []

            if skill_evidence:

                related_evidence.append({
                    "skill": related_skill,
                    "evidence": skill_evidence
                })

        if direct_evidence:

            status = "strong"

            reason = (
                "The resume contains direct evidence in "
                "experience, projects, or education that "
                "supports this responsibility."
            )

        elif related_evidence:

            status = "related"

            reason = (
                "The resume contains related skills, "
                "but does not explicitly demonstrate "
                "the full responsibility."
            )

        else:

            status = "missing"

            reason = (
                "No direct or meaningful related evidence "
                "was detected in the resume."
            )

        results.append({
            "responsibility": responsibility,
            "status": status,
            "evidence": direct_evidence,
            "related_evidence": related_evidence,
            "reason": reason,
        })

    summary = {
        "strong": sum(
            r["status"] == "strong"
            for r in results
        ),
        "related": sum(
            r["status"] == "related"
            for r in results
        ),
        "missing": sum(
            r["status"] == "missing"
            for r in results
        ),
        "unknown": sum(
            r["status"] == "unknown"
            for r in results
        ),
    }

    return {
        "responsibilities": results,
        "summary": summary,
    }


# ============================================================
# RESUME SCREENING
# ============================================================


def screen_resume(
    resume_text,
    job_description
):

    # --------------------------------------------------------
    # 1. Semantic similarity
    # --------------------------------------------------------

    semantic_score = calculate_match_score(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # 2. Skill extraction and comparison
    # --------------------------------------------------------

    skill_result = compare_skills(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # 3. Evidence-aware skill score
    # --------------------------------------------------------

    required_skills = (
        skill_result["required_skills"]
    )

    skill_score_available = bool(
        required_skills
    )

    skill_score = calculate_skill_score(
        skill_result["matched_skills"],
        required_skills,
        skill_result.get(
            "skill_evidence_levels",
            {}
        )
    )

    # --------------------------------------------------------
    # 4. Final compatibility score
    # --------------------------------------------------------

    final_score = calculate_final_score(
        semantic_score,
        skill_score,
        skill_score_available
    )

    # --------------------------------------------------------
    # 5. BERT category prediction
    # --------------------------------------------------------

    bert_categories = predict_top_categories(
        resume_text,
        top_k=3
    )

    category = (
        bert_categories[0]["category"]
        if bert_categories
        else "Unknown"
    )

    category_confidence = (
        bert_categories[0]["confidence"]
        if bert_categories
        else 0.0
    )

    # --------------------------------------------------------
    # 6. Generate recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        skill_result["matched_skills"],
        skill_result["missing_skills"],
        semantic_score,
        skill_score,
        required_skills,
        skill_evidence_levels=skill_result.get(
            "skill_evidence_levels",
            {}
        )
    )

    # --------------------------------------------------------
    # 7. Capability Intelligence
    # --------------------------------------------------------

    capability_results = analyze_capabilities(
        skill_result["resume_skills"]
    )

    # --------------------------------------------------------
    # 8. Job Responsibility Analysis
    # --------------------------------------------------------

    responsibility_analysis = (
        analyze_job_responsibilities(
            resume_text,
            job_description
        )
    )

    # --------------------------------------------------------
    # 9. Complete screening report
    # --------------------------------------------------------

    return {

        # ----------------------------------------------------
        # Compatibility scores
        # ----------------------------------------------------

        "final_score":
            final_score,

        "semantic_score":
            semantic_score,

        "skill_score":
            skill_score,

        "skill_score_available":
            skill_score_available,

        # ----------------------------------------------------
        # Candidate category
        # ----------------------------------------------------

        "category":
            category,

        "category_confidence":
            category_confidence,

        "bert_categories":
            bert_categories,

        # ----------------------------------------------------
        # Required job skills
        # ----------------------------------------------------

        "required_skills":
            required_skills,

        "matched_skills":
            skill_result["matched_skills"],

        "related_skills":
            skill_result.get(
                "related_skills",
                []
            ),

        "missing_skills":
            skill_result["missing_skills"],

        "skill_evidence":
            skill_result.get(
                "skill_evidence",
                {}
            ),

        # IMPORTANT:
        # Pass evidence classification to the UI.

        "skill_evidence_levels":
            skill_result.get(
                "skill_evidence_levels",
                {}
            ),

        "required_skill_evidence_levels":
            skill_result.get(
                "required_skill_evidence_levels",
                {}
            ),

        # ----------------------------------------------------
        # Preferred job skills
        # ----------------------------------------------------

        "preferred_skills":
            skill_result.get(
                "preferred_skills",
                []
            ),

        "preferred_matched_skills":
            skill_result.get(
                "preferred_matched_skills",
                []
            ),

        "preferred_related_skills":
            skill_result.get(
                "preferred_related_skills",
                []
            ),

        "preferred_missing_skills":
            skill_result.get(
                "preferred_missing_skills",
                []
            ),

        "preferred_skill_evidence":
            skill_result.get(
                "preferred_skill_evidence",
                {}
            ),

        # ----------------------------------------------------
        # Candidate-specific skill intelligence
        # ----------------------------------------------------

        "candidate_strengths":
            skill_result.get(
                "candidate_strengths",
                []
            ),

        "candidate_related":
            skill_result.get(
                "candidate_related",
                []
            ),

        "candidate_gaps":
            skill_result.get(
                "candidate_gaps",
                []
            ),

        # ----------------------------------------------------
        # Resume skills
        # ----------------------------------------------------

        "resume_skills":
            skill_result["resume_skills"],

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        "strengths":
            recommendations["strengths"],

        "skill_gaps":
            recommendations["skill_gaps"],

        "suggestions":
            recommendations["suggestions"],

        "score_explanation":
            recommendations.get(
                "score_explanation",
                []
            ),

        # ----------------------------------------------------
        # Capability Intelligence
        # ----------------------------------------------------

        "capabilities":
            capability_results,

        # ----------------------------------------------------
        # Job Responsibility Analysis
        # ----------------------------------------------------

        "responsibility_analysis":
            responsibility_analysis,
    }


# ============================================================
# SIMPLE TEST
# ============================================================


if __name__ == "__main__":

    print(
        "\nScreening Engine loaded successfully."
    )

    print(
        "Capability Intelligence: ENABLED"
    )

    print(
        "Compatibility Score: ENABLED"
    )

    print(
        "Evidence-Aware Skill Scoring: ENABLED"
    )

    print(
        "Semantic Matching: ENABLED"
    )

    print(
        "Skill Matching: ENABLED"
    )

    print(
        "BERT Classification: ENABLED"
    )

    print(
        "Recommendations: ENABLED"
    )

    print(
        "Job Responsibility Analysis: ENABLED"
    )