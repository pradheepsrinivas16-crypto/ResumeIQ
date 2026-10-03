from semantic_skill_matcher import (
    calculate_similarity_matrix
)


# ============================================================
# CONFIGURATION
# ============================================================

HIGH_CONFIDENCE_THRESHOLD = 0.80
REVIEW_THRESHOLD = 0.70


# ============================================================
# EVIDENCE-AWARE SEMANTIC MATCHING
# ============================================================

def classify_semantic_match(similarity):
    """
    Classify a semantic similarity score.

    Returns:
        high_confidence
        review
        weak
    """

    if similarity >= HIGH_CONFIDENCE_THRESHOLD:
        return "high_confidence"

    if similarity >= REVIEW_THRESHOLD:
        return "review"

    return "weak"


# ============================================================
# ANALYZE SKILLS
# ============================================================

def analyze_semantic_evidence(
    resume_skills,
    required_skills
):
    """
    Analyze semantic relationships between
    resume skills and required skills.

    This function DOES NOT modify the
    existing skill matcher or final score.
    """

    if not resume_skills or not required_skills:

        return {
            "high_confidence_matches": [],
            "review_matches": [],
            "weak_matches": [],
            "missing_skills": required_skills
        }

    similarity_matrix = calculate_similarity_matrix(
        resume_skills,
        required_skills
    )

    high_confidence_matches = []

    review_matches = []

    weak_matches = []

    for required_index, required_skill in enumerate(
        required_skills
    ):

        scores = similarity_matrix[
            required_index
        ]

        best_index = scores.argmax()

        best_score = float(
            scores[best_index]
        )

        best_resume_skill = resume_skills[
            best_index
        ]

        classification = classify_semantic_match(
            best_score
        )

        result = {
            "required_skill": required_skill,
            "resume_skill": best_resume_skill,
            "similarity": best_score,
            "classification": classification
        }

        if classification == "high_confidence":

            high_confidence_matches.append(
                result
            )

        elif classification == "review":

            review_matches.append(
                result
            )

        else:

            weak_matches.append(
                result
            )

    return {
        "high_confidence_matches":
            high_confidence_matches,

        "review_matches":
            review_matches,

        "weak_matches":
            weak_matches
    }


# ============================================================
# DISPLAY RESULTS
# ============================================================

def print_analysis(result):

    print("\n" + "=" * 70)
    print("EVIDENCE-AWARE SEMANTIC ANALYSIS")
    print("=" * 70)

    print("\nHIGH-CONFIDENCE MATCHES")

    if result["high_confidence_matches"]:

        for match in result[
            "high_confidence_matches"
        ]:

            print(
                f"  ✓ "
                f"{match['required_skill']}"
                f" ← "
                f"{match['resume_skill']}"
                f" "
                f"({match['similarity']:.3f})"
            )

    else:

        print("  None")

    print("\nREVIEW MATCHES")

    if result["review_matches"]:

        for match in result[
            "review_matches"
        ]:

            print(
                f"  ? "
                f"{match['required_skill']}"
                f" ← "
                f"{match['resume_skill']}"
                f" "
                f"({match['similarity']:.3f})"
            )

    else:

        print("  None")

    print("\nWEAK / UNMATCHED")

    if result["weak_matches"]:

        for match in result[
            "weak_matches"
        ]:

            print(
                f"  ✗ "
                f"{match['required_skill']}"
                f" ← "
                f"{match['resume_skill']}"
                f" "
                f"({match['similarity']:.3f})"
            )

    else:

        print("  None")

    print("\n" + "=" * 70)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    resume_skills = [
        "python",
        "sql",
        "power bi",
        "data analysis",
        "machine learning",
        "dashboard",
        "pandas",
        "numpy"
    ]

    required_skills = [
        "python",
        "sql",
        "data visualization",
        "dashboard development",
        "machine learning",
        "tableau",
        "statistical analysis"
    ]

    result = analyze_semantic_evidence(
        resume_skills,
        required_skills
    )

    print_analysis(result)