import re

DISPLAY_SKILL_NAMES = {
    "ui/ux": "UI/UX",
    "rest api": "REST API",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "aws": "AWS",
    "gcp": "GCP",
    "ci/cd": "CI/CD",
    "power bi": "Power BI",
    "api": "API",
    "kpi": "KPI",
    "eda": "EDA",
    "nlp": "NLP",
    "mlops": "MLOps",
    "gd&t": "GD&T",
    "cad": "CAD",
    "seo": "SEO",
    "sem": "SEM",
    "hris": "HRIS",
    "numpy": "NumPy",
    "pandas": "Pandas"
}

def format_skill_display(name):
    if not name:
        return ""
    norm = str(name).strip().lower()
    if norm in DISPLAY_SKILL_NAMES:
        return DISPLAY_SKILL_NAMES[norm]
    return str(name).strip().title()

SKILL_ALIASES = {
    "python": ["python", "python programming", "python 3"],
    "java": ["java", "java programming", "core java"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c#": ["c#", "c sharp"],
    "javascript": ["javascript", "java script", "js"],
    "typescript": ["typescript", "type script", "ts"],
    "html": ["html", "html5", "hypertext markup language"],
    "css": ["css", "css3", "cascading style sheets"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angularjs", "angular.js"],
    "node.js": ["node.js", "nodejs", "node js"],
    "rest api": ["rest api", "rest apis", "restful api", "restful apis", "rest services"],
    "spring boot": ["spring boot", "springboot", "spring-boot"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask", "flask framework"],
    "django": ["django", "django framework"],
    "ui/ux": ["ui/ux", "ui ux", "user interface and user experience", "user interface/user experience", "user interface", "user experience"],
    "responsive web design": [
        "responsive web design", "responsive web development", "responsive websites",
        "responsive web applications", "responsive web", "responsive design",
        "responsive e-commerce", "responsive ecommerce", "responsive"
    ],
    "figma": ["figma"],
    "adobe xd": ["adobe xd", "adobe experience design"],
    "canva": ["canva"],
    "postman": ["postman"],
    "jira": ["jira", "atlassian jira"],
    "vs code": ["vs code", "visual studio code", "vscode"],
    "intellij idea": ["intellij idea", "intellij"],
    "eclipse": ["eclipse ide", "eclipse"],
    "sql": ["sql", "structured query language", "mysql", "postgresql", "postgres", "sqlite"],
    "database": ["database", "databases", "relational database", "relational databases", "database management", "sql", "mysql", "postgresql"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres", "postgre sql"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "redis": ["redis"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "machine learning": ["machine learning", "machine-learning", "ml"],
    "deep learning": ["deep learning", "deep-learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "artificial-intelligence", "ai"],
    "natural language processing": ["natural language processing", "natural-language processing", "nlp"],
    "computer vision": ["computer vision", "computer-vision", "cv"],
    "data analysis": ["data analysis", "data analytics", "data analyst"],
    "data visualization": [
        "data visualization", "data visualizations", "data visualisation", "data visualisations",
        "visualizations", "visualization", "visualisation", "visualising data", "visualizing data"
    ],
    "data cleaning": ["data cleaning", "data cleansing", "data preprocessing", "data pre-processing"],
    "exploratory data analysis": ["exploratory data analysis", "exploratory analysis", "eda"],
    "statistical analysis": ["statistical analysis", "statistics", "statistical modelling", "statistical modeling", "statistical models"],
    "predictive modeling": ["predictive modeling", "predictive modelling", "predictive analytics", "random forest"],
    "model deployment": ["model deployment", "model deployments", "ml model deployment", "machine learning model deployment"],
    "mlops": ["mlops", "ml ops", "machine learning operations"],
    "model serving": ["model serving", "ml model serving"],
    "cloud computing": ["cloud computing", "cloud", "cloud technology", "cloud technologies"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["google cloud", "google cloud platform", "gcp"],
    "docker": ["docker", "docker containers", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": ["ci/cd", "ci cd", "continuous integration", "continuous delivery"],
    "jenkins": ["jenkins"],
    "github actions": ["github actions", "github action"],
    "linux": ["linux", "ubuntu"],
    "git": ["git", "git version control", "version control", "git workflows", "git workflow"],
    "github": ["github", "git hub"],
    "gitlab": ["gitlab", "git lab"],
    "excel": ["excel", "microsoft excel", "ms excel"],
    "power bi": ["power bi", "powerbi", "microsoft power bi", "power-bi"],
    "tableau": ["tableau"],
    "dashboard": ["dashboard", "dashboards", "dashboard development", "dashboarding", "bi dashboard"],
    "kpi": ["kpi", "kpis", "key performance indicator", "key performance indicators", "key metrics", "business metrics"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "torch"],
}

RELATED_SKILLS = {
    "machine learning": ["deep learning", "scikit-learn", "pytorch", "tensorflow", "predictive modeling"],
    "deep learning": ["machine learning", "pytorch", "tensorflow", "computer vision", "natural language processing"],
    "data analysis": ["pandas", "numpy", "data visualization", "statistical analysis", "data cleaning", "exploratory data analysis"],
    "data visualization": ["matplotlib", "seaborn", "power bi", "tableau", "dashboard"],
    "statistical analysis": ["exploratory data analysis", "data analysis", "python", "numpy", "pandas"],
    "rest api": ["backend development", "fastapi", "flask", "node.js", "spring boot"],
}

EQUIVALENT_TOOL_MAP = {
    "sql": {"mysql", "postgresql", "oracle", "sqlite", "sql server"},
    "database": {"mysql", "postgresql", "oracle", "sqlite", "sql server", "sql", "mongodb"},
    "adobe xd": {"figma", "sketch", "invision"},
    "figma": {"adobe xd", "sketch", "invision"},
    "sketch": {"figma", "adobe xd"},
    "power bi": {"tableau", "looker", "qlik"},
    "tableau": {"power bi", "looker", "qlik"},
    "postgresql": {"mysql", "oracle", "sqlite", "sql server", "sql"},
    "mysql": {"postgresql", "oracle", "sqlite", "sql server", "sql"},
    "react": {"angular", "vue", "svelte"},
    "angular": {"react", "vue", "svelte"},
    "vue": {"react", "angular", "svelte"},
    "fastapi": {"flask", "django"},
    "flask": {"fastapi", "django"},
}

def find_equivalent_skill(target_skill, available_skills):
    if not target_skill or not available_skills:
        return None
    target_clean = str(target_skill).strip().lower()
    available_set = {str(s).strip().lower() for s in available_skills}

    if target_clean in EQUIVALENT_TOOL_MAP:
        matches = EQUIVALENT_TOOL_MAP[target_clean].intersection(available_set)
        if matches:
            return next(iter(matches))

    for canonical, substitutes in EQUIVALENT_TOOL_MAP.items():
        if canonical in available_set and target_clean in substitutes:
            return canonical

    return None

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

RESUME_SECTION_HEADINGS = {
    "internship": "internship",
    "internships": "internship",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "projects": "projects",
    "project": "projects",
    "academic projects": "projects",
    "skills": "skills",
    "technical skills": "skills",
    "technical skill": "skills",
    "core competencies": "skills",
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
    "internship": "supporting",
    "experience": "strong",
    "projects": "strong",
    "skills": "listed",
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
        heading = re.sub(r"^[\s•\-*#●]+", "", clean).strip()
        heading_normalized = heading.rstrip(":").strip().lower()

        if heading_normalized in RESUME_SECTION_HEADINGS:
            current_section = RESUME_SECTION_HEADINGS[heading_normalized]
            continue

        sections[current_section].append(clean)

    return {key: "\n".join(value) for key, value in sections.items()}

MONTH_REGEX = r"\b(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\b"

def clean_evidence_sentence(sentence):
    """Sanitizes snippet while preserving intra-word hyphens and joining wrapped fragments."""
    if not sentence:
        return ""
    text = str(sentence).strip()
    text = re.sub(r"^(Present|Current|Date:?)\s*", "", text, flags=re.I)
    text = re.sub(r"[\u2022\u25cf\u25cb\u25e6\u2023\u25b8●*#]+\s*", " ", text)
    text = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "", text)
    text = re.sub(MONTH_REGEX + r"\s*\d{2,4}\b", "", text, flags=re.I)
    text = re.sub(r"\b(19|20)\d{2}\s*[-–—]\s*(Present|(19|20)\d{2})\b", "", text, flags=re.I)
    text = re.sub(r"\b(19|20)\d{2}\b", "", text)
    text = re.sub(r"(?<![a-zA-Z0-9])[-–—]+(?![a-zA-Z0-9])", " ", text)
    text = re.sub(r"(^\s*[:;,.\s]+|[:;,.\s]+$)", "", text).strip()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skill_snippet(text, aliases, max_len=280):
    if not text:
        return ""
    
    # 1. First join wrapped lines that don't start with bullet markers
    lines = text.splitlines()
    joined_blocks = []
    current_block = []

    for line in lines:
        l_str = line.strip()
        if not l_str:
            continue
        is_bullet_start = bool(re.match(r"^[\u2022\u25cf\u25cb\u25e6\u2023\u25b8●•\-*#]", l_str))
        if is_bullet_start and current_block:
            joined_blocks.append(" ".join(current_block))
            current_block = [l_str]
        else:
            current_block.append(l_str)
    if current_block:
        joined_blocks.append(" ".join(current_block))

    full_text = "\n".join(joined_blocks) if joined_blocks else text
    raw_units = re.split(r"\n+|[\u2022\u25cf\u25cb\u25e6\u2023\u25b8●•]|(?<=[.!?])\s+", full_text)
    
    ACTION_VERBS = {
        "built", "designed", "analyzed", "developed", "implemented", 
        "performed", "created", "optimized", "managed", "queried", 
        "automated", "visualize", "visualized", "track", "tracking", 
        "conducted", "spearheaded", "engineered", "generated", "clean", "cleaned"
    }
    
    action_units = []
    descriptive_units = []
    header_units = []

    for unit in raw_units:
        clean_unit = clean_evidence_sentence(unit)
        if len(clean_unit) < 15:
            continue
        unit_lower = clean_unit.lower()
        
        is_metadata = any(term in unit_lower for term in [
            "novitech ltd", "technopark", "pvt ltd", "1stop remote", 
            "intern —", "intern -", "technologies ltd"
        ])
        if is_metadata:
            continue

        has_alias = False
        for alias in aliases:
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias.lower()) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, unit_lower):
                has_alias = True
                break
        
        if has_alias:
            words = set(re.findall(r"\b[a-zA-Z]+\b", unit_lower))
            has_action = bool(words.intersection(ACTION_VERBS))
            
            # If line has parenthesized tech tags like "(Python, Web Tech)" and no action verb, categorize as header
            if ("(" in clean_unit and ")" in clean_unit) and not has_action:
                header_units.append(clean_unit)
            elif has_action:
                action_units.append(clean_unit)
            else:
                descriptive_units.append(clean_unit)

    # STRICT PRIORITY: Choose action bullet sentence first, then descriptive sentence, and only header as last resort
    chosen = action_units[0] if action_units else (descriptive_units[0] if descriptive_units else (header_units[0] if header_units else ""))
    
    if chosen:
        if len(chosen) > max_len:
            # Cut at full sentence or major punctuation
            cut = chosen[:max_len]
            punct_pos = max(cut.rfind("."), cut.rfind(";"), cut.rfind(","))
            if punct_pos > int(max_len * 0.65):
                return cut[:punct_pos + 1].strip()
            if " " in cut:
                return cut.rsplit(" ", 1)[0] + "..."
            return cut + "..."
        return chosen
    return ""

def find_contextual_skill_evidence(resume_text, skill):
    sections = extract_resume_sections(resume_text)
    aliases = SKILL_ALIASES.get(skill, [skill])
    evidence = []

    for section_name in ["projects", "experience", "internship", "certifications", "education", "skills"]:
        section_text = sections.get(section_name, "")
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
                    "snippet": snippet if snippet else f"Referenced {format_skill_display(alias)} in {section_name}.",
                    "strength": SECTION_STRENGTH.get(section_name, "supporting"),
                })
                break
        if evidence:
            break

    return evidence

def classify_skill_evidence(resume_text, skill):
    sections = extract_resume_sections(resume_text)
    aliases = SKILL_ALIASES.get(skill, [skill])
    found_sections = []

    for section_name in ["skills", "projects", "experience", "internship", "certifications", "education"]:
        section_text = sections.get(section_name, "")
        if not section_text.strip():
            continue

        normalized_section = normalize_text(section_text)
        for alias in aliases:
            alias_norm = normalize_text(alias)
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, normalized_section):
                found_sections.append(section_name)
                break

    found_sections = list(dict.fromkeys(found_sections))
    strong_sections = {"projects", "experience"}
    strong_found = [s for s in found_sections if s in strong_sections]

    if strong_found:
        substantive_body = "\n".join(sections[k] for k in strong_found if k in sections)
        snippet = extract_skill_snippet(substantive_body, aliases)
        if snippet:
            return {
                "status": "demonstrated",
                "sections": strong_found,
                "snippet": snippet,
                "confidence": 1.0,
            }
        
        # When skill is in project header/tech tag, extract that EXACT line verbatim
        tag_snippet = ""
        for line in substantive_body.splitlines():
            line_clean = line.strip()
            if any(re.search(r"(?<![a-zA-Z0-9])" + re.escape(a.lower()) + r"(?![a-zA-Z0-9])", line_clean.lower()) for a in aliases):
                tag_snippet = clean_evidence_sentence(line_clean)
                break

        return {
            "status": "supporting",
            "sections": strong_found,
            "snippet": tag_snippet if tag_snippet else f"Referenced in {strong_found[0]} tech summary.",
            "confidence": 0.70,
        }

    supporting_sections = {"internship", "certifications", "education"}
    supporting_found = [s for s in found_sections if s in supporting_sections]
    if supporting_found:
        substantive_body = "\n".join(sections[k] for k in supporting_found if k in sections)
        snippet = extract_skill_snippet(substantive_body, aliases)
        if not snippet:
            lines = [l.strip() for l in substantive_body.splitlines() if l.strip()]
            snippet = clean_evidence_sentence(lines[0]) if lines else f"Referenced in {supporting_found[0]}."
        return {
            "status": "supporting",
            "sections": supporting_found,
            "snippet": snippet,
            "confidence": 0.70,
        }

    candidate_all_skills = extract_skills(resume_text)
    substitute_tool = find_equivalent_skill(skill, candidate_all_skills)
    if substitute_tool:
        return {
            "status": "substitute",
            "sections": ["projects"],
            "substitute_tool": substitute_tool,
            "snippet": f"Demonstrates {format_skill_display(substitute_tool)}, satisfying this requirement via industry equivalence.",
            "confidence": 0.75,
        }

    if "skills" in found_sections:
        snippet_note = "Found in Skills inventory without active project sentence context."
        if skill in {"sql", "database"} and "mysql" in normalize_text(sections.get("skills", "")):
            snippet_note = "Found in Skills inventory (via MySQL) without active project sentence context."
        return {
            "status": "listed",
            "sections": ["skills"],
            "snippet": snippet_note,
            "confidence": 0.40,
        }

    return {
        "status": "missing",
        "sections": [],
        "snippet": "",
        "confidence": 0.0,
    }

def find_skill_evidence(text, skill):
    text = normalize_text(text)
    aliases = SKILL_ALIASES.get(skill, [skill])
    evidence = []
    for alias in aliases:
        alias_norm = normalize_text(alias)
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias_norm) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text):
            evidence.append(alias_norm)
    return evidence

def extract_skills(text):
    sections = extract_resume_sections(text)
    substantive_text = "\n".join(
        sections[s] for s in ["skills", "projects", "experience", "internship", "certifications", "education"]
    )
    norm_text = normalize_text(substantive_text)
    detected_skills = set()

    for skill in SKILL_ALIASES:
        evidence = find_skill_evidence(norm_text, skill)
        if evidence:
            detected_skills.add(skill)

    # In resume, if MySQL or PostgreSQL is detected, add SQL and Database to the skill inventory
    if "mysql" in detected_skills or "postgresql" in detected_skills:
        detected_skills.add("sql")
        detected_skills.add("database")

    return sorted(detected_skills)

def _extract_section(text, headings):
    lines = text.replace("\r", "\n").splitlines()
    target = {h.lower() for h in headings}
    current = None
    collected = {h: [] for h in target}
    stop_words = {"responsibilities", "requirements", "qualifications", "preferred skills", "required skills", "nice to have", "education", "experience"}

    for line in lines:
        clean = re.sub(r"^[\s•\-*#●]+", "", line).strip()
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
    norm_text = normalize_text(text)
    detected_skills = set()
    for skill in SKILL_ALIASES:
        # Prevent false positive: Only extract 'database' if 'database' explicitly exists in the text
        if skill == "database" and not re.search(r"\bdatabases?\b", norm_text):
            continue
        evidence = find_skill_evidence(text, skill)
        if evidence:
            detected_skills.add(skill)
    return sorted(detected_skills)

def parse_job_skill_sections(job_description):
    required_sections = _extract_section(job_description, ["required skills", "required skill", "requirements", "required qualifications", "key requirements"])
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

    # Handle ANY-OF GROUPS: Slash delimiters and 'or' (e.g. Tableau/PowerBI, Figma or Adobe XD)
    lower_jd = job_description.lower()
    
    # BI Tools: Tableau / PowerBI
    if ("tableau/powerbi" in lower_jd or "powerbi/tableau" in lower_jd or "tableau / power bi" in lower_jd or "tableau or power bi" in lower_jd or "power bi or tableau" in lower_jd):
        if "tableau" in required_skills and "power bi" in required_skills:
            # Coalesce into one single requirement: 'power bi' or 'tableau'
            required_skills.remove("tableau")

    # UI Tools: Figma or Adobe XD
    if ("figma or adobe xd" in lower_jd or "adobe xd or figma" in lower_jd or "figma/adobe xd" in lower_jd):
        if "figma" in required_skills and "adobe xd" in required_skills:
            required_skills.remove("adobe xd")

    return required_skills, preferred_skills

def compare_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    skill_evidence_levels = {}

    for skill in resume_skills:
        skill_evidence_levels[skill] = classify_skill_evidence(resume_text, skill)

    resume_skill_set = set(resume_skills)
    required_skills, preferred_skills = parse_job_skill_sections(job_description)

    matched = []
    missing = []
    req_levels = {}

    for skill in required_skills:
        ev = classify_skill_evidence(resume_text, skill)
        
        if ev["status"] == "missing":
            alt = find_equivalent_skill(skill, resume_skill_set)
            if alt:
                ev = {
                    "status": "substitute",
                    "substitute_tool": alt,
                    "sections": ["projects"],
                    "snippet": f"Demonstrates {format_skill_display(alt)}, satisfying this requirement via industry equivalence.",
                    "confidence": 0.75
                }

        req_levels[skill] = ev

        if ev["status"] != "missing":
            matched.append(skill)
        else:
            missing.append(skill)

    return {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": sorted(matched),
        "related_skills": [],
        "missing_skills": sorted(missing),
        "skill_evidence": {},
        "skill_evidence_levels": skill_evidence_levels,
        "required_skill_evidence_levels": req_levels,
        "preferred_skills": preferred_skills,
        "preferred_matched_skills": [],
        "preferred_related_skills": [],
        "preferred_missing_skills": preferred_skills,
        "preferred_skill_evidence": {},
    }