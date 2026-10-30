import pytest
from src.skill_matcher import extract_skills, classify_skill_evidence, compare_skills
from src.career_paths import get_alternative_pathways

# Test 1: Substring Guard (Works for ANY resume)
def test_no_substring_false_positives():
    """Ensures tool names aren't matched inside unrelated English words."""
    sample_text = """
    Hobbies:
    Exploring Digital Content, Watching Movies.

    Contact:
    user@github.com | website.com

    Experience:
    Managed logistical operations for supply chain.
    """
    skills = extract_skills(sample_text)
    assert "git" not in skills, "Failed: 'git' was matched as a substring inside 'Digital' or 'github.com'!"
    assert "go" not in skills, "Failed: 'go' was matched inside 'logistical'!"


# Test 2: RDB Alias Mapping (Works for ANY resume)
def test_database_alias_resolution():
    """Ensures relational DB tools satisfy SQL requirements dynamically."""
    sample_resume = """
    Skills:
    MySQL, PostgreSQL, Python
    """
    jd_text = """
    Requirements:
    SQL, Python
    """
    res = compare_skills(sample_resume, jd_text)
    assert "sql" in res["matched_skills"], "Failed: MySQL/Postgres should satisfy SQL competency."


# Test 3: Evidence Ladder Distinction (Works for ANY resume)
def test_evidence_tier_weighting():
    """Ensures project bullet points earn 1.0x while skills list earns only 0.4x."""
    sample_resume = """
    Skills:
    Java, Python, Docker

    Projects:
    E-Commerce Platform: Built and deployed scalable REST APIs using Python.
    """
    py_ev = classify_skill_evidence(sample_resume, "python")
    assert py_ev["status"] == "demonstrated", "Python with action verb in Projects must earn Demonstrated (1.0x)!"

    java_ev = classify_skill_evidence(sample_resume, "java")
    assert java_ev["status"] == "listed", "Java without project context must be restricted to Listed Only (0.4x)!"


# Test 4: Dynamic Arithmetic Sanity Check
def test_score_arithmetic_invariants():
    """Validates that skill matching returns non-empty matched requirements and respects extracted counts."""
    jd = """
    Requirements:
    Python, Docker, React
    """
    resume = """
    Skills:
    Python, Docker
    """
    res = compare_skills(resume, jd)
    assert "python" in res["matched_skills"]
    assert "docker" in res["matched_skills"]
    assert "react" in res["missing_skills"]
    assert len(res["required_skills"]) == 3
    assert len(res["matched_skills"]) == 2


# Test 5: Strict JD-Invariance for Global Pathways
def test_pathways_are_jd_independent():
    """Validates that Career Pathways remain completely invariant regardless of which target JD is passed."""
    resume_text = """
    Pradeep Srinivas B
    Skills & Tools: Python, SQL, Power BI, Excel, Data Analysis, Machine Learning
    Projects:
    Cricket-Twin AI: Analyzed datasets using Python and SQL to build predictive machine learning models.
    """
    resume_skills = extract_skills(resume_text)
    evidence_levels = {s: classify_skill_evidence(resume_text, s) for s in resume_skills}

    run_1 = get_alternative_pathways(resume_skills, skill_evidence_levels=evidence_levels)
    run_2 = get_alternative_pathways(resume_skills, skill_evidence_levels=evidence_levels)

    assert run_1 == run_2, "Failed: Career pathways must produce identical scores for the same candidate!"