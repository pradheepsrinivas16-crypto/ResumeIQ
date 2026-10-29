from src.skill_matcher import SKILL_ALIASES


# ============================================================
# ROLE PROFILES
# Core skills are the non-negotiable skills for the role.
# Supporting skills add significant weight but are secondary.
# ============================================================

ROLE_PROFILES = {
    "Data Analyst": {
        "core": ["python", "sql", "data analysis", "data visualization"],
        "supporting": ["pandas", "numpy", "excel", "power bi", "statistical analysis", "dashboard"],
    },

    "Data Scientist": {
        "core": ["python", "machine learning", "data analysis", "statistical analysis"],
        "supporting": ["pandas", "numpy", "scikit-learn", "predictive modeling", "data visualization"],
    },

    "Machine Learning Engineer": {
        "core": ["python", "machine learning", "deep learning"],
        "supporting": ["scikit-learn", "pytorch", "tensorflow", "model deployment", "mlops", "model serving"],
    },

    "Business Intelligence Analyst": {
        "core": ["sql", "power bi", "data visualization", "data analysis"],
        "supporting": ["excel", "tableau", "dashboard", "kpi"],
    },

    "Full Stack Developer": {
        "core": ["javascript", "html", "css", "sql"],
        "supporting": ["java", "react", "node.js", "mysql", "rest api", "spring boot", "git", "github"],
    },

    "Frontend Developer": {
        "core": ["html", "css", "javascript", "react"],
        "supporting": ["typescript", "git", "github"],
    },

    "Backend Developer": {
        "core": ["java", "spring boot", "rest api"],
        "supporting": ["node.js", "sql", "mysql", "git", "github"],
    },

    "Software Engineer": {
        "core": ["java", "python", "javascript"],
        "supporting": ["sql", "git", "github", "rest api"],
    },

    "Mechanical Design Engineer": {
        "core": ["mechanical engineering", "autocad", "solidworks"],
        "supporting": ["catia", "cad", "3d modeling", "gd&t", "manufacturing", "engineering drawings", "mechanical design"],
    },
}

# Evidence weights used when scoring with evidence levels
EVIDENCE_WEIGHTS = {
    "demonstrated": 1.00,
    "supporting": 0.75,
    "listed": 0.50,
    "listed_only": 0.50,
    "missing": 0.00,
}

# Weight of core skills vs supporting skills in the final role score
CORE_WEIGHT = 0.70
SUPPORTING_WEIGHT = 0.30


# ============================================================
# CANONICALIZE RESUME SKILLS
# ============================================================

def canonicalize_resume_skills(resume_skills):
    """
    Convert aliases into the canonical skill names used
    by ROLE_PROFILES.
    """

    alias_to_canonical = {}

    for canonical, aliases in SKILL_ALIASES.items():

        canonical_key = canonical.lower().strip()

        alias_to_canonical[canonical_key] = canonical

        for alias in aliases:
            alias_to_canonical[
                alias.lower().strip()
            ] = canonical

    canonical_skills = set()

    for skill in resume_skills:

        normalized = skill.lower().strip()

        canonical_skills.add(
            alias_to_canonical.get(
                normalized,
                normalized
            )
        )

    return canonical_skills


# ============================================================
# CALCULATE ROLE SUITABILITY (WEIGHTED)
# ============================================================

def calculate_role_suitability(resume_skills, role_name, skill_evidence_levels=None):
    """
    Calculate weighted role suitability using core/supporting
    skill distinction plus optional evidence strength weighting.

    Core skills carry 70% of the score; supporting skills 30%.
    Within each group, evidence levels (Demonstrated/Listed Only)
    further modulate the weight so a Listed-Only skill gets
    partial credit rather than full credit.
    """

    if role_name not in ROLE_PROFILES:
        raise ValueError(
            f"Unknown role: {role_name}"
        )

    profile = ROLE_PROFILES[role_name]
    core_required = set(profile["core"])
    supporting_required = set(profile["supporting"])
    all_required = core_required | supporting_required

    # --------------------------------------------------------
    # Candidate skills
    # --------------------------------------------------------

    candidate_skills = canonicalize_resume_skills(
        resume_skills
    )

    # --------------------------------------------------------
    # Evidence levels lookup helper
    # --------------------------------------------------------

    ev_levels = skill_evidence_levels or {}

    def get_evidence_weight(skill):
        """Return evidence weight for a skill (0.0–1.0)."""
        if not ev_levels:
            # No evidence data: treat a matched skill as fully demonstrated
            return 1.0 if skill in candidate_skills else 0.0
        ev = ev_levels.get(skill)
        if ev is None:
            # Case-insensitive fallback
            for k, v in ev_levels.items():
                if str(k).strip().lower() == skill.lower().strip():
                    ev = v
                    break
        if ev is None:
            # If matched but no evidence record, treat as listed_only
            if skill in candidate_skills:
                return EVIDENCE_WEIGHTS["listed_only"]
            return 0.0
        status = str(ev.get("status", "missing")).strip().lower()
        if status not in EVIDENCE_WEIGHTS:
            return 1.0 if skill in candidate_skills else 0.0
        return EVIDENCE_WEIGHTS[status]

    # --------------------------------------------------------
    # Core skill score  (0.0 – 1.0)
    # --------------------------------------------------------

    if core_required:
        core_score_sum = sum(
            get_evidence_weight(skill)
            for skill in core_required
            if skill in candidate_skills
        )
        core_score = core_score_sum / len(core_required)
    else:
        core_score = 0.0

    # --------------------------------------------------------
    # Supporting skill score  (0.0 – 1.0)
    # --------------------------------------------------------

    if supporting_required:
        sup_score_sum = sum(
            get_evidence_weight(skill)
            for skill in supporting_required
            if skill in candidate_skills
        )
        sup_score = sup_score_sum / len(supporting_required)
    else:
        sup_score = 0.0

    # --------------------------------------------------------
    # Weighted coverage
    # --------------------------------------------------------

    weighted_coverage = (
        core_score * CORE_WEIGHT
        + sup_score * SUPPORTING_WEIGHT
    ) * 100

    # --------------------------------------------------------
    # Simple matched / missing (for display)
    # --------------------------------------------------------

    matched_skills = sorted(
        candidate_skills.intersection(all_required)
    )

    missing_skills = sorted(
        all_required - candidate_skills
    )

    core_matched = sorted(candidate_skills.intersection(core_required))
    core_missing = sorted(core_required - candidate_skills)
    sup_matched = sorted(candidate_skills.intersection(supporting_required))
    sup_missing = sorted(supporting_required - candidate_skills)

    # --------------------------------------------------------
    # STRICT ROLE-FIT CLASSIFICATION
    # Based on weighted score, not raw count
    # --------------------------------------------------------

    if weighted_coverage >= 85:
        status = "Strong Fit"
    elif weighted_coverage >= 55:
        status = "Moderate Fit"
    else:
        status = "Poor Fit"

    return {
        "role": role_name,
        "coverage": weighted_coverage,
        "core_coverage": core_score * 100,
        "supporting_coverage": sup_score * 100,
        "status": status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "core_matched": core_matched,
        "core_missing": core_missing,
        "supporting_matched": sup_matched,
        "supporting_missing": sup_missing,
    }


# ============================================================
# RECOMMEND ROLES
# ============================================================

def recommend_roles(resume_skills, skill_evidence_levels=None):

    results = [
        calculate_role_suitability(
            resume_skills,
            role_name,
            skill_evidence_levels=skill_evidence_levels
        )
        for role_name in ROLE_PROFILES
    ]

    # Highest weighted coverage first.
    # If coverage is equal, prefer the role with
    # more matched skills.
    # Tie-break by coverage first, then total matched skills, then fewest missing
    results.sort(
        key=lambda x: (
            x["coverage"],
            len(x.get("matched_skills", [])),
            -len(x.get("missing_skills", []))
        ),
        reverse=True
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_skills = [
        "artificial intelligence",
        "aws",
        "cloud computing",
        "css",
        "deep learning",
        "github",
        "html",
        "java",
        "javascript",
        "mysql",
        "python",
        "react",
    ]

    print("=" * 70)
    print("ROLE SUITABILITY TEST (WEIGHTED)")
    print("=" * 70)

    results = recommend_roles(
        test_skills
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"{index}. "
            f"{result['role']} | "
            f"Weighted: {result['coverage']:.1f}% | "
            f"Core: {result['core_coverage']:.1f}% | "
            f"Sup: {result['supporting_coverage']:.1f}% | "
            f"{result['status']} | "
            f"Matched: {result['matched_skills']} | "
            f"Missing: {result['missing_skills']}"
        )