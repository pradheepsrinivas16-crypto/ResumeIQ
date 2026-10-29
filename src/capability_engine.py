from pathlib import Path
import sys

# ============================================================
# PATH SETUP
# ============================================================

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

# ============================================================
# IMPORTS
# ============================================================

from .resume_parser import extract_resume_text
from .skill_matcher import extract_skills

# ============================================================
# CAPABILITY DEFINITIONS
# ============================================================

CAPABILITIES = {
    # --------------------------------------------------------
    # SOFTWARE / WEB
    # --------------------------------------------------------
    "frontend development": {
        "description": (
            "Ability to build user-facing web interfaces using "
            "HTML, CSS, JavaScript and modern frontend frameworks."
        ),
        "core_skills": {
            "html",
            "css",
            "javascript"
        },
        "supporting_skills": {
            "react",
            "angular",
            "vue",
            "responsive web design",
            "ui/ux",
            "typescript"
        },
        "minimum_core": 2,
        "minimum_supporting": 1
    },

    "backend development": {
        "description": (
            "Ability to develop server-side applications, "
            "backend services and application logic."
        ),
        "core_skills": {
            "spring boot",
            "node.js"
        },
        "supporting_skills": {
            "rest api",
            "java",
            "sql",
            "mysql",
            "python"
        },
        "minimum_core": 1,
        "minimum_supporting": 0
    },

    "full stack development": {
        "description": (
            "Ability to combine frontend and backend development "
            "to build complete web applications."
        ),
        "core_skills": {
            "html",
            "css",
            "javascript",
            "spring boot",
            "node.js"
        },
        "supporting_skills": {
            "react",
            "angular",
            "rest api",
            "java",
            "mysql",
            "sql"
        },
        "minimum_core": 4,
        "minimum_supporting": 0
    },

    "database development": {
        "description": (
            "Ability to work with relational databases and "
            "database-driven applications."
        ),
        "core_skills": {
            "sql",
            "mysql"
        },
        "supporting_skills": {
            "crud",
            "mongodb",
            "postgresql",
            "database",
            "database management"
        },
        "minimum_core": 1,
        "minimum_supporting": 1
    },

    "api development": {
        "description": (
            "Ability to design or integrate application "
            "programming interfaces and backend services."
        ),
        "core_skills": {
            "rest api"
        },
        "supporting_skills": {
            "java",
            "spring boot",
            "node.js",
            "javascript"
        },
        "minimum_core": 1,
        "minimum_supporting": 1
    },

    "ui ux development": {
        "description": (
            "Ability to design usable and visually effective "
            "interfaces using UI/UX principles and design tools."
        ),
        "core_skills": {
            "figma",
            "ui/ux"
        },
        "supporting_skills": {
            "responsive web design",
            "html",
            "css",
            "javascript",
            "adobe xd",
            "canva"
        },
        "minimum_core": 1,
        "minimum_supporting": 1
    },

    "cloud development": {
        "description": (
            "Ability to work with cloud platforms and cloud-based "
            "application infrastructure."
        ),
        "core_skills": {
            "aws"
        },
        "supporting_skills": {
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "cloud"
        },
        "minimum_core": 1,
        "minimum_supporting": 1
    },

    "version control": {
        "description": (
            "Ability to manage source code and collaborate using "
            "version-control platforms."
        ),
        "core_skills": {
            "git",
            "github"
        },
        "supporting_skills": {
            "gitlab",
            "bitbucket",
            "version control"
        },
        "minimum_core": 1,
        "minimum_supporting": 0
    },

    # --------------------------------------------------------
    # DATA / AI
    # --------------------------------------------------------
    "data science": {
        "description": (
            "Ability to work with data using programming, "
            "data analysis, statistics and machine learning."
        ),
        "core_skills": {
            "python",
            "data analysis",
            "machine learning"
        },
        "supporting_skills": {
            "pandas",
            "numpy",
            "scikit-learn",
            "statistical analysis",
            "predictive modeling"
        },
        "minimum_core": 2,
        "minimum_supporting": 1
    },

    "data analytics": {
        "description": (
            "Ability to analyze data, identify trends and "
            "communicate insights using analytical tools."
        ),
        "core_skills": {
            "data analysis",
            "sql",
            "data visualization"
        },
        "supporting_skills": {
            "excel",
            "power bi",
            "tableau",
            "dashboard",
            "statistical analysis",
            "data cleaning",
            "exploratory data analysis"
        },
        "minimum_core": 2,
        "minimum_supporting": 1
    },

    "machine learning": {
        "description": (
            "Ability to develop predictive models using "
            "machine learning algorithms and data."
        ),
        "core_skills": {
            "machine learning",
            "python"
        },
        "supporting_skills": {
            "scikit-learn",
            "pandas",
            "numpy",
            "predictive modeling",
            "data analysis"
        },
        "minimum_core": 2,
        "minimum_supporting": 1
    },

    "business intelligence": {
        "description": (
            "Ability to transform business data into "
            "dashboards, reports and actionable insights."
        ),
        "core_skills": {
            "power bi",
            "dashboard"
        },
        "supporting_skills": {
            "sql",
            "excel",
            "tableau",
            "data visualization",
            "kpi",
            "data analysis"
        },
        "minimum_core": 1,
        "minimum_supporting": 2
    },

    "data visualization": {
        "description": (
            "Ability to communicate information through "
            "charts, dashboards and visual representations."
        ),
        "core_skills": {
            "data visualization"
        },
        "supporting_skills": {
            "power bi",
            "tableau",
            "matplotlib",
            "seaborn",
            "dashboard",
            "excel"
        },
        "minimum_core": 1,
        "minimum_supporting": 1
    }
}

# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skills(skills):
    if not skills:
        return set()

    return {
        str(skill).lower().strip()
        for skill in skills
        if str(skill).strip()
    }

# ============================================================
# ANALYZE ONE CAPABILITY
# ============================================================

def analyze_capability(resume_skills, capability_name):
    resume_skills = normalize_skills(resume_skills)
    capability = CAPABILITIES.get(capability_name)

    if capability is None:
        return {
            "capability": capability_name,
            "description": "",
            "supported": False,
            "core_matches": [],
            "supporting_matches": [],
            "missing_core": [],
            "missing_supporting": [],
            "evidence_count": 0
        }

    core_skills = set(capability["core_skills"])
    supporting_skills = set(capability["supporting_skills"])

    core_matches = sorted(resume_skills.intersection(core_skills))
    supporting_matches = sorted(resume_skills.intersection(supporting_skills))
    missing_core = sorted(core_skills - resume_skills)
    missing_supporting = sorted(supporting_skills - resume_skills)

    core_requirement_met = len(core_matches) >= capability["minimum_core"]
    supporting_requirement_met = len(supporting_matches) >= capability["minimum_supporting"]

    supported = core_requirement_met and supporting_requirement_met

    if capability_name == "backend development":
        supported = supported and bool(resume_skills.intersection({"spring boot", "node.js"}))

    if capability_name == "full stack development":
        supported = (
            supported
            and {"html", "css", "javascript"}.issubset(resume_skills)
            and bool(resume_skills.intersection({"spring boot", "node.js"}))
        )

    evidence_count = len(core_matches) + len(supporting_matches)

    return {
        "capability": capability_name,
        "description": capability["description"],
        "supported": supported,
        "core_matches": core_matches,
        "supporting_matches": supporting_matches,
        "missing_core": missing_core,
        "missing_supporting": missing_supporting,
        "evidence_count": evidence_count
    }

# ============================================================
# ANALYZE ALL CAPABILITIES
# ============================================================

def analyze_capabilities(resume_skills):
    results = []
    for capability_name in CAPABILITIES:
        results.append(analyze_capability(resume_skills, capability_name))
    return results

# ============================================================
# JOB-RELEVANT CAPABILITY ANALYSIS
# ============================================================

def analyze_job_relevant_capabilities(resume_skills, job_skills):
    resume_skills = normalize_skills(resume_skills)
    job_skills = normalize_skills(job_skills)

    if not job_skills:
        return []

    # Harmonize Git/GitHub/Version Control aliases
    if any(g in resume_skills for g in ["git", "github", "gitlab"]):
        resume_skills.add("git")
        resume_skills.add("version control")

    results = []

    for capability_name, capability in CAPABILITIES.items():
        core_skills = set(capability["core_skills"])
        supporting_skills = set(capability["supporting_skills"])
        capability_skills = core_skills | supporting_skills

        relevant_job_skills = sorted(job_skills.intersection(capability_skills))
        if not relevant_job_skills:
            continue

        matched = []
        for s in relevant_job_skills:
            if s in resume_skills:
                matched.append(s)
            elif s in {"git", "version control"} and any(g in resume_skills for g in ["git", "github", "gitlab", "version control"]):
                matched.append(s)
            # Credit valid industry substitutes within capability view
            elif s == "adobe xd" and "figma" in resume_skills:
                matched.append("adobe xd (Sub: Figma)")
            elif s == "power bi" and "tableau" in resume_skills:
                matched.append("power bi (Sub: Tableau)")
            elif s == "mysql" and "postgresql" in resume_skills:
                matched.append("mysql (Sub: PostgreSQL)")

        matched = sorted(list(set(matched)))
        
        # Calculate true missing excluding any substituted skills
        missing = []
        for s in relevant_job_skills:
            if not any(s == m or m.startswith(f"{s} (Sub:") for m in matched):
                missing.append(s)
        missing = sorted(list(set(missing)))

        coverage = (len(matched) / len(relevant_job_skills) * 100) if relevant_job_skills else 0.0

        if coverage >= 99.9:
            alignment = "Strong Alignment"
        elif coverage >= 45:
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