# ============================================================
# SCREENING ENGINE
# ============================================================

try:
    # Used when imported as:
    # from src.screening_engine import screen_resume

    from .job_matcher import calculate_match_score
    from .skill_matcher import compare_skills
    from .bert_category_predictor import predict_top_categories
    from .recommendations import generate_recommendations
    from .capability_engine import analyze_capabilities

except ImportError:
    # Used when running directly:
    # python src/screening_engine.py

    from job_matcher import calculate_match_score
    from skill_matcher import compare_skills
    from bert_category_predictor import predict_top_categories
    from recommendations import generate_recommendations
    from capability_engine import analyze_capabilities


# ============================================================
# SKILL SCORE
# ============================================================

def calculate_skill_score(
    matched_skills,
    required_skills
):

    if not required_skills:
        return 0.0

    return (
        len(matched_skills)
        / len(required_skills)
        * 100
    )


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(
    semantic_score,
    skill_score,
    semantic_weight=0.60,
    skill_weight=0.40
):

    return (
        semantic_score * semantic_weight
        + skill_score * skill_weight
    )


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
    # 3. Skill score
    # --------------------------------------------------------

    skill_score = calculate_skill_score(
        skill_result["matched_skills"],
        skill_result["required_skills"]
    )


    # --------------------------------------------------------
    # 4. Final compatibility score
    # --------------------------------------------------------

    final_score = calculate_final_score(
        semantic_score,
        skill_score
    )


    # --------------------------------------------------------
    # 5. BERT category prediction
    # --------------------------------------------------------
    #
    # BERT predicts the most likely resume categories.
    #
    # IMPORTANT:
    # BERT category confidence is NOT the compatibility
    # score and does NOT affect the compatibility calculation.
    # --------------------------------------------------------

    bert_categories = predict_top_categories(
        resume_text,
        top_k=3
    )

    category = bert_categories[0]["category"]

    category_confidence = bert_categories[0]["confidence"]


    # --------------------------------------------------------
    # 6. Generate recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
    skill_result["matched_skills"],
    skill_result["missing_skills"],
    semantic_score,
    skill_score,
    skill_result["required_skills"]
)

    # --------------------------------------------------------
    # 7. Capability Intelligence
    # --------------------------------------------------------
    #
    # This analyzes the skills detected in the actual resume
    # and identifies higher-level capabilities.
    #
    # It DOES NOT change the compatibility score.
    # --------------------------------------------------------

    capability_results = analyze_capabilities(
        skill_result["resume_skills"]
    )


    # --------------------------------------------------------
    # 8. Complete screening report
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
        # Job skill analysis
        # ----------------------------------------------------

        "required_skills":
            skill_result["required_skills"],

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],


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


        # ----------------------------------------------------
        # Capability Intelligence
        # ----------------------------------------------------

        "capabilities":
            capability_results
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