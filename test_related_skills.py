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


def find_related_skills(required_skill, resume_skills):

    related = RELATED_SKILLS.get(required_skill, [])

    return [
        skill
        for skill in resume_skills
        if skill in related
    ]


# ==============================
# TEST CASES
# ==============================

tests = [
    (
        "machine learning",
        ["python", "deep learning", "pytorch"]
    ),

    (
        "computer vision",
        ["python", "opencv", "deep learning"]
    ),

    (
        "data analysis",
        ["python", "pandas", "numpy"]
    ),

    (
        "data visualization",
        ["power bi", "dashboard", "excel"]
    ),

    (
        "machine learning",
        ["python", "sql"]
    ),
]


print("=" * 60)
print("RELATED SKILL MATCHING TEST")
print("=" * 60)

for required_skill, resume_skills in tests:

    related = find_related_skills(
        required_skill,
        resume_skills
    )

    print("\nJD Skill:", required_skill)
    print("Resume Skills:", resume_skills)
    print("Related Skills:", related)

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)