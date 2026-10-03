import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

# These are intentionally conservative.
HIGH_CONFIDENCE = 0.80
RELATED_CONFIDENCE = 0.65


# ============================================================
# MODEL
# ============================================================

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# SKILL RELATIONSHIP DESCRIPTIONS
# ============================================================
#
# Instead of comparing only:
#
#     "python" <-> "data science"
#
# we give the model contextual descriptions.
#
# This allows us to test whether the concepts are related.
# ============================================================

SKILL_CONTEXTS = {

    "python": (
        "Python programming language used for "
        "software development, data analysis, "
        "data science, machine learning, automation "
        "and scripting."
    ),

    "data science": (
        "Data science involves analyzing data, "
        "statistics, machine learning, predictive "
        "modeling, programming and extracting "
        "insights from datasets."
    ),

    "data analytics": (
        "Data analytics involves collecting, cleaning, "
        "analyzing and visualizing data to identify "
        "patterns, trends and business insights."
    ),

    "data analysis": (
        "Data analysis involves examining, cleaning, "
        "transforming and interpreting data to "
        "generate useful insights."
    ),

    "machine learning": (
        "Machine learning uses algorithms and data "
        "to build predictive models and discover "
        "patterns automatically."
    ),

    "pandas": (
        "Pandas is a Python library used for "
        "data manipulation, data cleaning, "
        "data analysis and tabular data processing."
    ),

    "numpy": (
        "NumPy is a Python library for numerical "
        "computing, arrays, mathematical operations "
        "and scientific data processing."
    ),

    "scikit-learn": (
        "Scikit-learn is a Python machine learning "
        "library used for classification, regression, "
        "clustering, preprocessing and model evaluation."
    ),

    "power bi": (
        "Power BI is a business intelligence and "
        "data visualization platform used to create "
        "interactive dashboards, reports and "
        "business analytics."
    ),

    "tableau": (
        "Tableau is a business intelligence and "
        "data visualization platform used to create "
        "interactive dashboards, reports and "
        "visual analytics."
    ),

    "data visualization": (
        "Data visualization involves representing "
        "data using charts, graphs, dashboards and "
        "interactive visual reports."
    ),

    "dashboard development": (
        "Dashboard development involves creating "
        "interactive dashboards and reports using "
        "business intelligence and visualization tools."
    ),

    "statistical analysis": (
        "Statistical analysis involves applying "
        "statistical methods to understand data, "
        "identify patterns and support conclusions."
    ),

    "excel": (
        "Microsoft Excel is a spreadsheet tool used "
        "for data analysis, calculations, reporting, "
        "data cleaning and visualization."
    )
}


# ============================================================
# GET CONTEXT
# ============================================================

def get_skill_context(skill):
    """
    Return a contextual description of a skill.

    If the skill does not have a predefined
    description, the skill name itself is used.
    """

    skill = skill.lower().strip()

    return SKILL_CONTEXTS.get(
        skill,
        skill
    )


# ============================================================
# CREATE CONTEXTUAL EMBEDDINGS
# ============================================================

def encode_skill_contexts(skills):
    """
    Convert skill descriptions into embeddings.
    """

    descriptions = [
        get_skill_context(skill)
        for skill in skills
    ]

    if not descriptions:

        return np.empty(
            (0, 384)
        )

    embeddings = model.encode(
        descriptions,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


# ============================================================
# CALCULATE CONTEXTUAL SIMILARITY
# ============================================================

def calculate_contextual_similarity(
    resume_skills,
    required_skills
):
    """
    Calculate semantic similarity using
    contextual skill descriptions.
    """

    if not resume_skills or not required_skills:

        return np.empty(
            (
                len(required_skills),
                len(resume_skills)
            )
        )

    resume_embeddings = encode_skill_contexts(
        resume_skills
    )

    required_embeddings = encode_skill_contexts(
        required_skills
    )

    similarity_matrix = cosine_similarity(
        required_embeddings,
        resume_embeddings
    )

    return similarity_matrix


# ============================================================
# CLASSIFY RELATIONSHIP
# ============================================================

def classify_relationship(score):
    """
    Classify contextual relationship.

    0.80+  = high confidence
    0.65+  = related
    below  = weak
    """

    if score >= HIGH_CONFIDENCE:

        return "high_confidence"

    if score >= RELATED_CONFIDENCE:

        return "related"

    return "weak"


# ============================================================
# ANALYZE RELATIONSHIPS
# ============================================================

def analyze_contextual_relationships(
    resume_skills,
    required_skills
):
    """
    Find the strongest contextual relationship
    for every required skill.
    """

    if not resume_skills or not required_skills:

        return []

    similarity_matrix = (
        calculate_contextual_similarity(
            resume_skills,
            required_skills
        )
    )

    results = []

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

        best_resume_skill = (
            resume_skills[best_index]
        )

        relationship = classify_relationship(
            best_score
        )

        results.append({

            "required_skill":
                required_skill,

            "resume_skill":
                best_resume_skill,

            "similarity":
                best_score,

            "relationship":
                relationship
        })

    return results


# ============================================================
# PRINT REPORT
# ============================================================

def print_contextual_report(results):

    print("\n" + "=" * 80)
    print("CONTEXTUAL SKILL RELATIONSHIP ANALYSIS")
    print("=" * 80)

    for result in results:

        required = result[
            "required_skill"
        ]

        resume = result[
            "resume_skill"
        ]

        score = result[
            "similarity"
        ]

        relationship = result[
            "relationship"
        ]

        print(
            f"{required:<30}"
            f" ← "
            f"{resume:<25}"
            f" {score:.3f}"
            f"  [{relationship}]"
        )

    print("=" * 80)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    resume_skills = [

        "python",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "data analysis",
        "power bi",
        "dashboard"
    ]

    required_skills = [

        "python",
        "data science",
        "data analytics",
        "machine learning",
        "data visualization",
        "dashboard development",
        "tableau",
        "statistical analysis"
    ]

    print("\n" + "=" * 80)
    print("CONTEXTUAL SKILL INTELLIGENCE TEST")
    print("=" * 80)

    print("\nResume Skills:")

    for skill in resume_skills:

        print(
            f"  ✓ {skill}"
        )

    print("\nRequired Skills:")

    for skill in required_skills:

        print(
            f"  • {skill}"
        )

    results = analyze_contextual_relationships(
        resume_skills,
        required_skills
    )

    print_contextual_report(
        results
    )

    # ========================================================
    # DETAILED INTERESTING RELATIONSHIPS
    # ========================================================

    print(
        "\nIMPORTANT RELATIONSHIPS"
    )

    interesting_pairs = [
        ("python", "data science"),
        ("python", "data analytics"),
        ("python", "machine learning"),
        ("power bi", "data visualization"),
        ("power bi", "dashboard development"),
        ("tableau", "data visualization"),
        ("pandas", "data analysis"),
        ("scikit-learn", "machine learning")
    ]

    print("\n")

    for skill_a, skill_b in interesting_pairs:

        matrix = calculate_contextual_similarity(
            [skill_a],
            [skill_b]
        )

        score = float(
            matrix[0][0]
        )

        relationship = classify_relationship(
            score
        )

        print(
            f"{skill_a:<20}"
            f" ↔ "
            f"{skill_b:<25}"
            f" {score:.3f}"
            f" [{relationship}]"
        )

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)