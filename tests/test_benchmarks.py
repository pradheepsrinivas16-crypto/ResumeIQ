import pytest
from src.skill_matcher import extract_skills, classify_skill_evidence, compare_skills, SKILL_ALIASES
from src.screening_engine import extract_job_responsibilities, analyze_job_responsibilities
from src.capability_engine import analyze_job_relevant_capabilities
from src.interview_generator import generate_interview_questions
from src.career_paths import get_alternative_pathways


# 1. Responsibility Parser & Tier Mapping
def test_responsibility_parser_excludes_requirements_and_uses_skill_tiers():
    jd = """
    Responsibilities:
    - Develop responsive web applications using HTML, CSS, and JavaScript.
    - Integrate backend REST APIs.

    Required Skills:
    - Strong foundation in HTML, CSS, and JavaScript.
    """
    duties = extract_job_responsibilities(jd)
    assert len(duties) == 2, f"Expected 2 duties, got {duties}"
    assert not any("Required Skills" in d for d in duties)

    resume = "Skills:\nHTML, CSS, JavaScript"
    resp_analysis = analyze_job_responsibilities(resume, jd)["responsibilities"]
    assert resp_analysis[0]["status"] == "related"
    assert "listed only" in resp_analysis[0]["related_evidence"][0]["skill"]
    assert resp_analysis[1]["status"] == "missing"


# 2. Verbatim Evidence Check (Never Generate Fake Text)
def test_every_evidence_quote_contains_skill_or_alias():
    resume = """
    Skills:
    Angular, MySQL

    Internship:
    JAVA Full stack Quest Innovative Solutions Trivandrum
    React JS | Srishti Innovative
    UI/UX | Srishti Innovative
    """
    for skill in ["java", "react", "ui/ux", "angular"]:
        ev = classify_skill_evidence(resume, skill)
        quote = ev.get("snippet", "").lower()
        assert "demonstrates" not in quote, f"Generated fake text found in quote: {quote}"
        aliases = [a.lower() for a in SKILL_ALIASES.get(skill, [skill])]
        assert any(a in quote for a in aliases), f"Quote '{quote}' does not contain {skill} or its aliases!"


# 3. Exact Line Extraction in Sections
def test_exact_line_matching_in_internship():
    resume = """
    Internship:
    JAVA Full stack Quest Innovative Solutions Trivandrum
    React JS | Srishti Innovative
    UI/UX | Srishti Innovative
    """
    react_ev = classify_skill_evidence(resume, "react")
    assert "React JS" in react_ev["snippet"]
    assert "JAVA Full stack" not in react_ev["snippet"]

    uiux_ev = classify_skill_evidence(resume, "ui/ux")
    assert "UI/UX" in uiux_ev["snippet"]


# 4. Any-Of Group Coalescing
def test_any_of_react_or_angular_counts_as_one():
    jd = "Required Skills:\nReact or Angular, Git"
    resume = "Skills:\nAngular\nInternship:\nReact JS | Srishti"
    res = compare_skills(resume, jd)
    assert len(res["required_skills"]) == 2
    assert "react" in res["required_skills"]
    assert "angular" not in res["required_skills"]


# 5. Interview Question Wording & No Duplicate Alternatives
def test_interview_question_design_wording():
    qs = generate_interview_questions(
        missing_skills=[],
        supporting_skills=["css"],
        supporting_evidence_map={
            "css": {"sections": ["projects"], "snippet": "E-cart Home page (HTML, CSS, JS)"}
        }
    )
    assert len(qs) == 1
    assert "layouts, components, or styles" in qs[0]["question"]
    assert "modules, logic, or functions" not in qs[0]["question"]


# 6. Consistent Capability Thresholds
def test_capability_40_percent_maps_to_low_alignment():
    caps = analyze_job_relevant_capabilities(
        resume_skills=["git"],
        job_skills=["git"],
        skill_evidence_levels={"git": {"status": "listed", "confidence": 0.40}}
    )
    vc = next(c for c in caps if c["capability"] == "Version Control")
    assert vc["coverage"] == 40.0
    assert vc["alignment"] == "Low Alignment"

def test_git_url_and_substring_guard():
    """Ensures github.com URLs and English words like 'Digital' never trigger false Git matches."""
    resume = "Contact: github.com/user\nHobbies: Digital art"
    skills = extract_skills(resume)
    assert "git" not in skills

def test_deterministic_repeat_execution():
    """Verifies identical outputs across repeated executions on the same resume and JD."""
    resume = "Skills: Python, SQL\nProjects:\nBuilt data pipelines using Python and SQL."
    jd = "Required Skills:\nPython, SQL, Power BI"
    res1 = compare_skills(resume, jd)
    res2 = compare_skills(resume, jd)
    assert res1 == res2

def test_backend_capability_requires_core_backend_skill():
    """Ensures Python + SQL alone without a backend framework caps at Partial Alignment."""
    caps = analyze_job_relevant_capabilities(
        resume_skills=["python", "sql"],
        job_skills=["python", "sql"],
        skill_evidence_levels={
            "python": {"status": "demonstrated", "confidence": 1.0},
            "sql": {"status": "demonstrated", "confidence": 1.0},
        }
    )
    be = next(c for c in caps if c["capability"] == "Backend Development")
    assert be["alignment"] == "Partial Alignment"
    assert be["coverage"] <= 55.0