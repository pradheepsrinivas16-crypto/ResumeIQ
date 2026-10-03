import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

DEFAULT_THRESHOLD = 0.70


# ============================================================
# MODEL
# ============================================================

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# ENCODING
# ============================================================

def encode_skills(skills):
    """
    Convert a list of skills into sentence embeddings.

    Returns:
        NumPy array containing embeddings.
    """

    if not skills:
        return np.empty((0, 384))

    embeddings = model.encode(
        skills,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


# ============================================================
# SIMILARITY MATRIX
# ============================================================

def calculate_similarity_matrix(
    resume_skills,
    required_skills
):
    """
    Calculate cosine similarity between every
    resume skill and every required skill.

    Returns:
        similarity matrix

    Shape:
        len(required_skills) x len(resume_skills)
    """

    if not resume_skills or not required_skills:
        return np.empty(
            (
                len(required_skills),
                len(resume_skills)
            )
        )

    resume_embeddings = encode_skills(
        resume_skills
    )

    required_embeddings = encode_skills(
        required_skills
    )

    similarity_matrix = cosine_similarity(
        required_embeddings,
        resume_embeddings
    )

    return similarity_matrix


# ============================================================
# BEST MATCH FOR ONE REQUIRED SKILL
# ============================================================

def find_best_semantic_match(
    resume_skills,
    required_skill,
    threshold=DEFAULT_THRESHOLD
):
    """
    Find the strongest semantic match for
    one required skill.
    """

    if not resume_skills:
        return None

    similarity_matrix = calculate_similarity_matrix(
        resume_skills,
        [required_skill]
    )

    scores = similarity_matrix[0]

    best_index = int(
        np.argmax(scores)
    )

    best_score = float(
        scores[best_index]
    )

    best_skill = resume_skills[
        best_index
    ]

    if best_score >= threshold:

        return {
            "required_skill": required_skill,
            "matched_skill": best_skill,
            "similarity": best_score,
            "match_type": "semantic"
        }

    return None


# ============================================================
# ALL SEMANTIC MATCHES
# ============================================================

def find_all_semantic_matches(
    resume_skills,
    required_skills,
    threshold=DEFAULT_THRESHOLD
):
    """
    Find the best semantic match for every
    required skill.

    Only matches above the threshold are returned.
    """

    if not resume_skills or not required_skills:
        return []

    similarity_matrix = calculate_similarity_matrix(
        resume_skills,
        required_skills
    )

    matches = []

    for required_index, required_skill in enumerate(
        required_skills
    ):

        scores = similarity_matrix[
            required_index
        ]

        best_index = int(
            np.argmax(scores)
        )

        best_score = float(
            scores[best_index]
        )

        best_skill = resume_skills[
            best_index
        ]

        if best_score >= threshold:

            matches.append(
                {
                    "required_skill": required_skill,
                    "matched_skill": best_skill,
                    "similarity": best_score,
                    "match_type": "semantic"
                }
            )

    return matches


# ============================================================
# COMPLETE SEMANTIC ANALYSIS
# ============================================================

def analyze_semantic_skills(
    resume_skills,
    required_skills,
    threshold=DEFAULT_THRESHOLD
):
    """
    Perform complete semantic skill analysis.

    Returns:

        semantic_matches
        semantic_missing
        similarity_matrix
    """

    if not required_skills:

        return {
            "semantic_matches": [],
            "semantic_missing": [],
            "similarity_matrix": []
        }

    similarity_matrix = calculate_similarity_matrix(
        resume_skills,
        required_skills
    )

    semantic_matches = []
    semantic_missing = []

    for required_index, required_skill in enumerate(
        required_skills
    ):

        scores = similarity_matrix[
            required_index
        ]

        if len(scores) == 0:

            semantic_missing.append(
                required_skill
            )

            continue

        best_index = int(
            np.argmax(scores)
        )

        best_score = float(
            scores[best_index]
        )

        best_skill = resume_skills[
            best_index
        ]

        if best_score >= threshold:

            semantic_matches.append(
                {
                    "required_skill": required_skill,
                    "matched_skill": best_skill,
                    "similarity": best_score,
                    "match_type": "semantic"
                }
            )

        else:

            semantic_missing.append(
                required_skill
            )

    return {
        "semantic_matches": semantic_matches,
        "semantic_missing": semantic_missing,
        "similarity_matrix": similarity_matrix
    }


# ============================================================
# DISPLAY SIMILARITY ANALYSIS
# ============================================================

def print_similarity_analysis(
    resume_skills,
    required_skills
):
    """
    Display the strongest semantic relationship
    for every required skill.

    This is mainly useful for model validation.
    """

    if not resume_skills:

        print("\nNo resume skills available.")

        return

    if not required_skills:

        print("\nNo required skills available.")

        return

    similarity_matrix = calculate_similarity_matrix(
        resume_skills,
        required_skills
    )

    print("\n" + "=" * 70)
    print("SEMANTIC SIMILARITY ANALYSIS")
    print("=" * 70)

    for required_index, required_skill in enumerate(
        required_skills
    ):

        scores = similarity_matrix[
            required_index
        ]

        best_index = int(
            np.argmax(scores)
        )

        best_score = float(
            scores[best_index]
        )

        best_skill = resume_skills[
            best_index
        ]

        print(
            f"{required_skill:<30}"
            f" ← "
            f"{best_skill:<25}"
            f" {best_score:.3f}"
        )

    print("=" * 70)


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

    print("\n" + "=" * 70)
    print("PROFESSIONAL SEMANTIC SKILL MATCHING TEST")
    print("=" * 70)

    print("\nResume Skills:")

    for skill in resume_skills:
        print("  ✓", skill)

    print("\nRequired Skills:")

    for skill in required_skills:
        print("  •", skill)

    # --------------------------------------------------------
    # Show strongest relationship for every required skill
    # --------------------------------------------------------

    print_similarity_analysis(
        resume_skills,
        required_skills
    )

    # --------------------------------------------------------
    # Threshold analysis
    # --------------------------------------------------------

    for threshold in [0.60, 0.70, 0.80, 0.85]:

        result = analyze_semantic_skills(
            resume_skills,
            required_skills,
            threshold=threshold
        )

        print(
            f"\nThreshold: {threshold:.2f}"
        )

        print(
            f"Semantic Matches: "
            f"{len(result['semantic_matches'])}"
        )

        print(
            f"Semantic Missing: "
            f"{len(result['semantic_missing'])}"
        )

        for match in result[
            "semantic_matches"
        ]:

            print(
                f"  ✓ "
                f"{match['required_skill']}"
                f" ← "
                f"{match['matched_skill']}"
                f" "
                f"({match['similarity']:.3f})"
            )

        for skill in result[
            "semantic_missing"
        ]:

            print(
                f"  ✗ {skill}"
            )

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)