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
    "spring boot": [
        "spring boot",
        "springboot",
        "spring-boot"
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
    "ui/ux": [
        "ui/ux",
        "ui ux",
        "user interface and user experience",
        "user interface/user experience",
        "user interface",
        "user experience"
    ],
    "responsive web design": [
        "responsive web design",
        "responsive web development",
        "responsive websites",
        "responsive web applications",
        "responsive web",
        "responsive design",
        "responsive e-commerce",
        "responsive ecommerce",
        "responsive"
    ],

    # --------------------------------------------------------
    # DESIGN & DEVELOPMENT TOOLS
    # --------------------------------------------------------
    "figma": [
        "figma"
    ],
    "adobe xd": [
        "adobe xd",
        "adobe experience design"
    ],
    "canva": [
        "canva"
    ],
    "postman": [
        "postman"
    ],
    "jira": [
        "jira",
        "atlassian jira"
    ],
    "vs code": [
        "vs code",
        "visual studio code",
        "vscode"
    ],
    "intellij idea": [
        "intellij idea",
        "intellij"
    ],
    "eclipse": [
        "eclipse ide",
        "eclipse"
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
        "git version control",
        "version control",
        "git workflows",
        "git workflow",
        "github workflows",
        "collaborative development"
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
    ],

    # --------------------------------------------------------
    # MECHANICAL ENGINEERING
    # --------------------------------------------------------
    "mechanical engineering": [
        "mechanical engineering",
        "mechanical engineer"
    ],
    "autocad": [
        "autocad",
        "auto cad"
    ],
    "solidworks": [
        "solidworks",
        "solid works"
    ],
    "catia": [
        "catia"
    ],
    "cad": [
        "cad",
        "computer aided design",
        "computer-aided design"
    ],
    "3d modeling": [
        "3d modeling",
        "3d modelling",
        "3d model",
        "3d cad"
    ],
    "gd&t": [
        "gd&t",
        "geometric dimensioning and tolerancing",
        "geometric dimensioning",
        "dimensioning and tolerancing"
    ],
    "manufacturing": [
        "manufacturing",
        "manufacturing processes",
        "manufacturing process"
    ],
    "engineering drawings": [
        "engineering drawings",
        "engineering drawing",
        "technical drawings",
        "technical drawing"
    ],
    "mechanical design": [
        "mechanical design",
        "mechanical component design",
        "component design"
    ],

    # --------------------------------------------------------
    # FINANCE
    # --------------------------------------------------------
    "financial analysis": [
        "financial analysis",
        "financial analyst"
    ],
    "financial modeling": [
        "financial modeling",
        "financial modelling",
        "financial model"
    ],
    "accounting": [
        "accounting",
        "accountancy"
    ],
    "financial reporting": [
        "financial reporting",
        "financial reports"
    ],

    # --------------------------------------------------------
    # MARKETING
    # --------------------------------------------------------
    "digital marketing": [
        "digital marketing",
        "online marketing"
    ],
    "seo": [
        "seo",
        "search engine optimization",
        "search engine optimisation"
    ],
    "sem": [
        "sem",
        "search engine marketing"
    ],
    "google analytics": [
        "google analytics",
        "ga4"
    ],
    "social media marketing": [
        "social media marketing",
        "social media management"
    ],

    # --------------------------------------------------------
    # HUMAN RESOURCES
    # --------------------------------------------------------
    "recruitment": [
        "recruitment",
        "recruiting",
        "recruiter"
    ],
    "talent acquisition": [
        "talent acquisition",
        "talent management"
    ],
    "payroll": [
        "payroll",
        "payroll management"
    ],
    "employee relations": [
        "employee relations"
    ],
    "hris": [
        "hris",
        "human resources information system"
    ],
}

# ============================================================
# RELATED SKILL RELATIONSHIPS
# ============================================================

RELATED_SKILLS = {
    "machine learning": [
        "deep learning",
        "scikit-learn",
        "pytorch",
        "tensorflow",
        "predictive modeling"
    ],
    "deep learning": [
        "machine learning",
        "pytorch",
        "tensorflow",
        "computer vision",
        "natural language processing"
    ],
    "computer vision": [
        "opencv",
        "deep learning",
        "pytorch",
        "tensorflow"
    ],
    "natural language processing": [
        "machine learning",
        "deep learning"
    ],
    "data analysis": [
        "pandas",
        "numpy",
        "data visualization",
        "statistical analysis",
        "data cleaning"
    ],
    "data visualization": [
        "matplotlib",
        "seaborn",
        "power bi",
        "tableau",
        "dashboard"
    ],
    "model deployment": [
        "mlops",
        "model serving",
        "machine learning"
    ]
}

# ============================================================
# SKILL EQUIVALENCE / INDUSTRY SUBSTITUTIONS
# ============================================================

EQUIVALENT_SKILLS = {
    "adobe xd": ["figma", "sketch", "invision"],
    "figma": ["adobe xd", "sketch", "invision"],
    "sketch": ["figma", "adobe xd"],
    "pytorch": ["tensorflow", "keras"],
    "tensorflow": ["pytorch", "keras"],
    "power bi": ["tableau", "looker", "qlik"],
    "tableau": ["power bi", "looker", "qlik"],
    "postgresql": ["mysql", "sql server", "oracle"],
    "mysql": ["postgresql", "sql server", "sqlite"],
    "aws": ["azure", "gcp", "google cloud"],
    "azure": ["aws", "gcp", "google cloud"],
    "gcp": ["aws", "azure", "google cloud"],
    "react": ["vue", "angular", "svelte"],
    "vue": ["react", "angular", "svelte"],
    "docker": ["podman", "containerization"],
    "fastapi": ["flask", "django"],
    "flask": ["fastapi", "django"],
}

def find_equivalent_skill(missing_skill, candidate_skills):
    clean_missing = str(missing_skill).strip().lower()
    clean_candidate = [str(s).strip().lower() for s in (candidate_skills or [])]

    if clean_missing in EQUIVALENT_SKILLS:
        for equiv in EQUIVALENT_SKILLS[clean_missing]:
            for cand_skill in clean_candidate:
                if equiv in cand_skill or cand_skill in equiv:
                    return equiv.title()
    return None

# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ============================================================
# FIND SKILL EVIDENCE
# ============================================================

def find_skill_evidence(text, skill):
    text = normalize_text(text)
    aliases = SKILL_ALIASES.get(skill, [skill])
    evidence = []
    for alias in aliases:
        alias = normalize_text(alias)
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text):
            evidence.append(alias)
    return evidence

# ============================================================
# RESUME SECTION DETECTION
# ============================================================

RESUME_SECTION_HEADINGS = {
    "internship": "internship",
    "internships": "internship",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "projects": "projects",
    "project": "projects",
    "skills": "skills",
    "technical skills": "skills",
    "technical skill": "skills",
    "certifications": "certifications",
    "certification": "certifications",
    "education": "education",
    "profile": "profile",
    "summary": "profile",
    "objective": "profile",
    "extra-curricular": "extra_curricular",
    "extra curricular": "extra_curricular",
    "extracurricular": "extra_curricular",
    "hobbies": "hobbies",
    "languages": "languages",
}

SECTION_STRENGTH = {
    "internship": "strong",
    "experience": "strong",
    "projects": "strong",
    "skills": "direct",
    "certifications": "supporting",
    "education": "supporting",
    "profile": "supporting",
    "extra_curricular": "supporting",
    "other": "supporting",
}

def extract_resume_sections(text):
    text = str(text or "").replace("\r", "\n")
    lines = text.splitlines()

    sections = {
        "contact": [],
        "profile": [],
        "internship": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "certifications": [],
        "soft_skills": [],
        "education": [],
        "extra_curricular": [],
        "hobbies": [],
        "languages": [],
        "other": [],
    }

    current_section = "contact"

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        heading = re.sub(r"^[\s•\-*#]+", "", clean).strip()
        heading_normalized = heading.rstrip(":").strip().lower()

        if heading_normalized in RESUME_SECTION_HEADINGS:
            current_section = RESUME_SECTION_HEADINGS[heading_normalized]
            continue

        sections[current_section].append(clean)

    return {key: "\n".join(value) for key, value in sections.items()}

def extract_skill_snippet(text, aliases, max_len=140):
    if not text:
        return ""
    raw_units = re.split(r"(?<=[.!?\n])\s+|[\u2022\u25E6\u2023\u25B8\u2013-]\s+", text)
    for unit in raw_units:
        clean_unit = re.sub(r"\s+", " ", unit).strip()
        if len(clean_unit) < 15:
            continue
        unit_lower = clean_unit.lower()
        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, unit_lower):
                if len(clean_unit) > max_len:
                    return clean_unit[:max_len].rsplit(" ", 1)[0] + "..."
                return clean_unit
    return ""

def find_contextual_skill_evidence(resume_text, skill):
    sections = extract_resume_sections(resume_text)
    aliases = SKILL_ALIASES.get(skill, [skill])
    evidence = []

    for section_name, section_text in sections.items():
        if section_name in {"contact", "soft_skills"}:
            continue
        if not section_text.strip():
            continue

        normalized_section = normalize_text(section_text)
        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, normalized_section):
                snippet = extract_skill_snippet(section_text, aliases)
                evidence.append({
                    "section": section_name,
                    "evidence": alias,
                    "snippet": snippet if snippet else f"Demonstrated {alias} in {section_name}.",
                    "strength": SECTION_STRENGTH.get(section_name, "supporting"),
                })
                break

    # Substantive fallback (checks full experience/project text)
    if not evidence:
        raw_lines = str(resume_text or "").replace("\r", "\n").splitlines()
        clean_lines = [
            line for line in raw_lines 
            if not re.search(r"https?://|www\.|@", line, flags=re.I)
        ]
        substantive_body = "\n".join(clean_lines)
        substantive_norm = normalize_text(substantive_body)

        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, substantive_norm):
                snippet = extract_skill_snippet(substantive_body, aliases)
                evidence.append({
                    "section": "projects",
                    "evidence": alias,
                    "snippet": snippet if snippet else f"Demonstrated {alias} in projects / experience.",
                    "strength": "strong",
                })
                break

    return evidence

def classify_skill_evidence(resume_text, skill):
    sections = extract_resume_sections(resume_text)
    aliases = SKILL_ALIASES.get(skill, [skill])

    found_sections = []

    for section_name, section_text in sections.items():
        if section_name in {"contact", "soft_skills"}:
            continue
        if not section_text.strip():
            continue

        normalized_section = normalize_text(section_text)
        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, normalized_section):
                found_sections.append(section_name)
                break

    # Substantive fallback
    if not found_sections:
        raw_lines = str(resume_text or "").replace("\r", "\n").splitlines()
        clean_lines = [
            line for line in raw_lines 
            if not re.search(r"https?://|www\.|@", line, flags=re.I)
        ]
        substantive_text = normalize_text("\n".join(clean_lines))

        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, substantive_text):
                found_sections.append("projects")
                break

    found_sections = list(dict.fromkeys(found_sections))

    strong_sections = {"projects", "experience", "internship"}
    strong_found = [s for s in found_sections if s in strong_sections]

    if strong_found:
        substantive_body = "\n".join(
            v for k, v in sections.items() if k in strong_sections
        )
        if not substantive_body.strip():
            substantive_body = str(resume_text or "")
        snippet = extract_skill_snippet(substantive_body, aliases)
        return {
            "status": "demonstrated",
            "sections": strong_found,
            "snippet": snippet if snippet else f"Demonstrated {skill} in project work.",
            "confidence": 1.0,
        }

    if "skills" in found_sections:
        return {
            "status": "listed",
            "sections": ["skills"],
            "confidence": 0.65,
        }

    supporting_sections = {"certifications", "education"}
    supporting_found = [s for s in found_sections if s in supporting_sections]

    if supporting_found:
        return {
            "status": "supporting",
            "sections": supporting_found,
            "confidence": 0.4,
        }

    # Substitute check
    candidate_all_skills = extract_skills(resume_text)
    substitute_tool = find_equivalent_skill(skill, candidate_all_skills)
    if substitute_tool:
        return {
            "status": "substitute",
            "sections": ["projects"],
            "substitute_tool": substitute_tool,
            "confidence": 0.75,
        }

    return {
        "status": "missing",
        "sections": [],
        "confidence": 0.0,
    }

def extract_skills(text):
    detected_skills = set()
    norm_text = normalize_text(text)

    for skill in SKILL_ALIASES:
        evidence = find_contextual_skill_evidence(text, skill)
        if evidence:
            detected_skills.add(skill)
        else:
            for alias in SKILL_ALIASES[skill]:
                alias_norm = normalize_text(alias)
                pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
                if re.search(pattern, norm_text):
                    detected_skills.add(skill)
                    break

    return sorted(detected_skills)

def _extract_section(text, headings):
    lines = text.replace("\r", "\n").splitlines()
    target = {h.lower() for h in headings}
    current = None
    collected = {h: [] for h in target}
    stop_words = {"responsibilities", "requirements", "qualifications", "preferred skills", "required skills", "nice to have", "education", "experience"}

    for line in lines:
        clean = re.sub(r"^[\s•\-*]+", "", line).strip()
        if not clean:
            continue
        heading = clean.rstrip(":").strip().lower()
        if heading in target:
            current = heading
            continue
        if current and heading in stop_words and heading not in target:
            current = None
            continue
        if current:
            collected[current].append(line)

    return {k: "\n".join(v) for k, v in collected.items()}

def extract_job_skills(text):
    detected_skills = set()
    for skill in SKILL_ALIASES:
        evidence = find_skill_evidence(text, skill)
        if evidence:
            detected_skills.add(skill)
    return sorted(detected_skills)

def parse_job_skill_sections(job_description):
    required_sections = _extract_section(job_description, ["required skills", "required skill", "requirements", "required qualifications"])
    preferred_sections = _extract_section(job_description, ["preferred skills", "preferred skill", "nice to have", "preferred qualifications"])

    required_text = "\n".join(v for v in required_sections.values() if v.strip())
    preferred_text = "\n".join(v for v in preferred_sections.values() if v.strip())

    if not required_text.strip():
        required_text = job_description

    required_skills = extract_job_skills(required_text)
    preferred_skills = (
        extract_job_skills(preferred_text)
        if preferred_text.strip()
        else []
    )
    preferred_skills = [s for s in preferred_skills if s not in required_skills]
    return required_skills, preferred_skills

def compare_skill_group(resume_text, skills, resume_skill_set):
    matched_skills = []
    related_skills = []
    missing_skills = []
    skill_evidence = {}

    for skill in skills:
        # 1. DIRECT EVIDENCE OR ALREADY RECOGNIZED IN RESUME
        evidence = find_contextual_skill_evidence(resume_text, skill)
        if evidence or (skill in resume_skill_set):
            matched_skills.append(skill)
            skill_evidence[skill] = {
                "type": "direct",
                "evidence": evidence if evidence else [{
                    "section": "projects", 
                    "evidence": skill, 
                    "snippet": f"Demonstrated {skill} in project or experience workflows.", 
                    "strength": "strong"
                }],
                "confidence": 1.0
            }
            continue

        # 2. VALID SUBSTITUTE TOOL (e.g. Figma for Adobe XD)
        substitute_tool = find_equivalent_skill(skill, resume_skill_set)
        if substitute_tool:
            matched_skills.append(skill)
            skill_evidence[skill] = {
                "type": "substitute",
                "substitute_tool": substitute_tool,
                "evidence": [{"section": "projects", "evidence": substitute_tool, "strength": "supporting"}],
                "confidence": 0.75
            }
            continue

        # 3. RELATED EVIDENCE
        related_found = [
            related for related in RELATED_SKILLS.get(skill, [])
            if related in resume_skill_set
        ]
        if related_found:
            related_skills.append(skill)
            skill_evidence[skill] = {
                "type": "related",
                "evidence": related_found,
                "confidence": 0.5
            }
            continue

        # 4. MISSING
        missing_skills.append(skill)
        skill_evidence[skill] = {
            "type": "missing",
            "evidence": [],
            "confidence": 0.0
        }

    return (
        matched_skills,
        related_skills,
        missing_skills,
        skill_evidence
    )

RESPONSIBILITY_PATTERNS = [
    {
        "name": "responsive web development",
        "patterns": [
            "responsive web",
            "responsive websites",
            "responsive applications",
            "responsive web applications",
        ],
        "related_skills": [
            "responsive web design",
            "html",
            "css",
            "javascript",
            "react",
        ],
    },
    {
        "name": "react frontend development",
        "patterns": [
            "frontend applications using react",
            "front-end applications using react",
            "frontend using react",
            "front end using react",
            "react frontend",
            "react front end",
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
            "rest api",
            "rest apis",
            "restful api",
            "restful apis",
            "api development",
            "apis",
        ],
        "related_skills": [
            "java",
            "spring boot",
            "node.js",
            "backend development",
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
            "sql",
            "database",
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
            "sql",
            "database",
        ],
    },
    {
        "name": "frontend backend integration",
        "patterns": [
            "integrate frontend applications with backend",
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
            "debug",
            "debugging",
            "test web applications",
            "testing web applications",
            "test and maintain",
            "testing",
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
            "git",
            "github",
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
        "related_skills": [
            "java",
            "spring boot",
            "react",
            "aws",
        ],
    },
]

def extract_job_responsibilities(job_description):
    text = str(job_description or "").replace("\r", "\n")
    lines = text.splitlines()
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

    for line in lines:
        clean = re.sub(r"^[\s•\-*]+", "", line).strip()
        if not clean:
            continue
        heading = clean.rstrip(":").strip().lower()

        if heading in {
            "responsibilities",
            "responsibility",
            "job responsibilities",
        }:
            in_responsibilities = True
            continue

        if in_responsibilities and heading in section_stops:
            in_responsibilities = False
            continue

        if in_responsibilities:
            responsibilities.append(clean)

    return responsibilities

def find_responsibility_rule(responsibility):
    normalized = normalize_text(responsibility)
    for rule in RESPONSIBILITY_PATTERNS:
        for pattern in rule["patterns"]:
            if pattern in normalized:
                return rule
    return None

def analyze_job_responsibilities(resume_text, job_description):
    responsibilities = extract_job_responsibilities(job_description)
    resume_sections = extract_resume_sections(resume_text)
    results = []

    for responsibility in responsibilities:
        rule = find_responsibility_rule(responsibility)
        if rule is None:
            results.append({
                "responsibility": responsibility,
                "status": "unknown",
                "evidence": [],
                "reason": "No safe responsibility rule is available for this requirement.",
            })
            continue

        direct_evidence = []
        related_evidence = []

        resume_full_content = "\n".join(
            value for key, value in resume_sections.items() if key != "contact"
        )
        normalized_resume = normalize_text(resume_full_content)

        for pattern in rule["patterns"]:
            if pattern in normalized_resume:
                direct_evidence.append({
                    "evidence": pattern,
                    "source": "resume",
                })

        resume_skills = set(extract_skills(resume_text))
        for related_skill in rule["related_skills"]:
            if related_skill in resume_skills:
                skill_evidence = find_contextual_skill_evidence(
                    resume_text,
                    related_skill
                )
                related_evidence.append({
                    "skill": related_skill,
                    "evidence": skill_evidence,
                })

        if direct_evidence:
            status = "strong"
            reason = "The resume explicitly demonstrates evidence related to this responsibility."
        elif related_evidence:
            status = "related"
            reason = "The resume contains related skills, but they do not by themselves prove the full responsibility."
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
        "strong": sum(1 for item in results if item["status"] == "strong"),
        "related": sum(1 for item in results if item["status"] == "related"),
        "missing": sum(1 for item in results if item["status"] == "missing"),
        "unknown": sum(1 for item in results if item["status"] == "unknown"),
    }

    return {
        "responsibilities": results,
        "summary": summary,
    }

def compare_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    skill_evidence_levels = {}

    for skill in resume_skills:
        skill_evidence_levels[skill] = classify_skill_evidence(resume_text, skill)

    resume_skill_set = set(resume_skills)
    required_skills, preferred_skills = parse_job_skill_sections(job_description)

    matched, related, missing, evidence = compare_skill_group(
        resume_text,
        required_skills,
        resume_skill_set
    )

    pref_matched, pref_related, pref_missing, pref_evidence = compare_skill_group(
        resume_text,
        preferred_skills,
        resume_skill_set
    )

    candidate_strengths = []
    for skill in matched:
        candidate_strengths.append({
            "skill": skill,
            "type": "direct",
            "evidence": evidence[skill]["evidence"]
        })

    candidate_related = []
    for skill in related:
        candidate_related.append({
            "skill": skill,
            "type": "related",
            "evidence": evidence[skill]["evidence"]
        })

    candidate_gaps = []
    for skill in missing:
        candidate_gaps.append({
            "skill": skill,
            "reason": "No direct or related evidence detected in the resume."
        })

    responsibility_analysis = analyze_job_responsibilities(resume_text, job_description)

    # Build required_skill_evidence_levels cleanly
    req_levels = {}
    for skill in required_skills:
        # Check direct matched skills first
        if skill in matched:
            if skill in evidence and evidence[skill].get("type") == "substitute":
                sub_tool = evidence[skill].get("substitute_tool", "Equivalent tool")
                req_levels[skill] = {
                    "status": "substitute",
                    "substitute_tool": sub_tool,
                    "sections": ["projects"],
                    "confidence": 0.75
                }
            elif skill in skill_evidence_levels and skill_evidence_levels[skill].get("status") in {"demonstrated", "listed", "supporting"}:
                req_levels[skill] = skill_evidence_levels[skill]
            else:
                snippet_text = ""
                if skill in evidence and evidence[skill].get("evidence"):
                    snippet_text = evidence[skill]["evidence"][0].get("snippet", "")
                req_levels[skill] = {
                    "status": "demonstrated",
                    "sections": ["projects"],
                    "snippet": snippet_text if snippet_text else f"Demonstrated {skill} in project workflows.",
                    "confidence": 1.0
                }
        elif skill in skill_evidence_levels and skill_evidence_levels[skill].get("status") != "missing":
            req_levels[skill] = skill_evidence_levels[skill]
        else:
            req_levels[skill] = {
                "status": "missing",
                "sections": [],
                "confidence": 0.0
            }

    return {
        "responsibility_analysis": responsibility_analysis,
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched,
        "related_skills": related,
        "missing_skills": missing,
        "skill_evidence": evidence,
        "skill_evidence_levels": skill_evidence_levels,
        "required_skill_evidence_levels": req_levels,
        "preferred_skills": preferred_skills,
        "preferred_matched_skills": pref_matched,
        "preferred_related_skills": pref_related,
        "preferred_missing_skills": pref_missing,
        "preferred_skill_evidence": pref_evidence,
        "candidate_strengths": candidate_strengths,
        "candidate_related": candidate_related,
        "candidate_gaps": candidate_gaps
    }