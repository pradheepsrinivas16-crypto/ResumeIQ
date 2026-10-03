import re


# ============================================================
# PROFESSIONAL SKILL TAXONOMY
# ============================================================

SKILL_ALIASES = {

    # --------------------------------------------------------
    # PROGRAMMING LANGUAGES
    # --------------------------------------------------------

    "python": [
        "python",
        "python programming",
        "python 3"
    ],

    "java": [
        "java",
        "java programming",
        "core java"
    ],

    "c": [
        "c programming",
        "c language"
    ],

    "c++": [
        "c++",
        "cpp",
        "c plus plus"
    ],

    "c#": [
        "c#",
        "c sharp"
    ],

    "javascript": [
        "javascript",
        "java script",
        "js"
    ],

    "typescript": [
        "typescript",
        "type script",
        "ts"
    ],

    # --------------------------------------------------------
    # WEB DEVELOPMENT
    # --------------------------------------------------------

    "html": [
        "html",
        "html5",
        "hypertext markup language"
    ],

    "css": [
        "css",
        "css3",
        "cascading style sheets"
    ],

    "react": [
        "react",
        "react.js",
        "reactjs"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest services"
    ],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "flask": [
        "flask",
        "flask framework"
    ],

    "django": [
        "django",
        "django framework"
    ],

    # --------------------------------------------------------
    # DATABASES
    # --------------------------------------------------------

    "sql": [
        "sql",
        "structured query language"
    ],

    "mysql": [
        "mysql",
        "my sql"
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgre sql"
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo"
    ],

    "redis": [
        "redis"
    ],

    "database": [
        "database",
        "databases",
        "database management"
    ],

    # --------------------------------------------------------
    # DATA SCIENCE
    # --------------------------------------------------------

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "matplotlib": [
        "matplotlib"
    ],

    "seaborn": [
        "seaborn"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
        "ai"
    ],

    "natural language processing": [
        "natural language processing",
        "natural-language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision",
        "computer-vision",
        "cv"
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
        "data analyst"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation",
        "visualization",
        "visualisation"
    ],

    "data cleaning": [
        "data cleaning",
        "data cleansing",
        "data preprocessing",
        "data pre-processing"
    ],

    "exploratory data analysis": [
        "exploratory data analysis",
        "exploratory analysis",
        "eda"
    ],

    "statistical analysis": [
        "statistical analysis",
        "statistics",
        "statistical modelling",
        "statistical modeling"
    ],

    "predictive modeling": [
        "predictive modeling",
        "predictive modelling",
        "predictive analytics"
    ],

    # --------------------------------------------------------
    # MACHINE LEARNING ENGINEERING
    # --------------------------------------------------------

    "model deployment": [
        "model deployment",
        "model deployments",
        "ml model deployment",
        "machine learning model deployment",
        "deploying models",
        "deployment of models"
    ],

    "mlops": [
        "mlops",
        "ml ops",
        "machine learning operations",
        "machine-learning operations"
    ],

    "model serving": [
        "model serving",
        "ml model serving",
        "machine learning model serving"
    ],

    # --------------------------------------------------------
    # CLOUD
    # --------------------------------------------------------

    "cloud computing": [
        "cloud computing",
        "cloud",
        "cloud technology",
        "cloud technologies"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "google cloud": [
        "google cloud",
        "google cloud platform",
        "gcp"
    ],

    # --------------------------------------------------------
    # DEVOPS
    # --------------------------------------------------------

    "docker": [
        "docker",
        "docker containers",
        "containerization",
        "containerisation"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment"
    ],

    "jenkins": [
        "jenkins"
    ],

    "github actions": [
        "github actions",
        "github action"
    ],

    "linux": [
        "linux",
        "ubuntu"
    ],

    # --------------------------------------------------------
    # VERSION CONTROL
    # --------------------------------------------------------

    "git": [
        "git",
        "git version control"
    ],

    "github": [
        "github",
        "git hub"
    ],

    "gitlab": [
        "gitlab",
        "git lab"
    ],

    # --------------------------------------------------------
    # BUSINESS INTELLIGENCE
    # --------------------------------------------------------

    "excel": [
        "excel",
        "microsoft excel",
        "ms excel"
    ],

    "power bi": [
        "power bi",
        "powerbi",
        "microsoft power bi",
        "power-bi"
    ],

    "tableau": [
        "tableau"
    ],

    "dashboard": [
        "dashboard",
        "dashboards",
        "dashboard development",
        "dashboarding",
        "bi dashboard",
        "bi dashboards"
    ],

    "kpi": [
        "kpi",
        "kpis",
        "key performance indicator",
        "key performance indicators"
    ],

    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch",
        "torch"
    ],

    "opencv": [
        "opencv",
        "open cv"
    ],

    "graphql": [
        "graphql",
        "graph ql"
    ],

    "spark": [
        "spark",
        "apache spark",
        "pyspark"
    ],

    "hadoop": [
        "hadoop",
        "apache hadoop"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FIND SKILL EVIDENCE
# ============================================================

def find_skill_evidence(
    text,
    skill
):

    text = normalize_text(text)

    aliases = SKILL_ALIASES.get(
        skill,
        [skill]
    )

    evidence = []

    for alias in aliases:

        alias = normalize_text(
            alias
        )

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            evidence.append(
                alias
            )

    return evidence


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):

    detected_skills = set()

    for skill in SKILL_ALIASES:

        evidence = find_skill_evidence(
            text,
            skill
        )

        if evidence:

            detected_skills.add(
                skill
            )

    return sorted(
        detected_skills
    )


# ============================================================
# COMPARE RESUME WITH JOB
# ============================================================

def compare_skills(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    required_skills = extract_skills(
        job_description
    )

    matched_skills = []

    missing_skills = []

    skill_evidence = {}

    for skill in required_skills:

        evidence = find_skill_evidence(
            resume_text,
            skill
        )

        if evidence:

            matched_skills.append(
                skill
            )

            skill_evidence[skill] = {
                "type": "exact_or_alias",
                "evidence": evidence
            }

        else:

            missing_skills.append(
                skill
            )

    return {

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_evidence": skill_evidence

    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\nProfessional Skill Matcher loaded."
    )

    print(
        f"Total canonical skills: "
        f"{len(SKILL_ALIASES)}"
    )