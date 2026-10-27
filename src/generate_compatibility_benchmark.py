from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RESUME_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "resume_clean.csv"
)

JOB_FILE = (
    PROJECT_DIR
    / "data"
    / "evaluation"
    / "job_descriptions.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "evaluation"
    / "compatibility_benchmark_raw.csv"
)


# ============================================================
# SETTINGS
# ============================================================

RESUMES_PER_JOB = 30
RANDOM_STATE = 42


# ============================================================
# CATEGORY GROUPS
# ============================================================

ROLE_CATEGORIES = {

    "JD001": {
        "relevant": [
            "INFORMATION-TECHNOLOGY",
            "FINANCE",
            "ACCOUNTANT"
        ],
        "adjacent": [
            "BUSINESS-DEVELOPMENT",
            "BANKING",
            "CONSULTANT"
        ]
    },

    "JD002": {
        "relevant": [
            "INFORMATION-TECHNOLOGY",
            "ENGINEERING"
        ],
        "adjacent": [
            "DESIGNER",
            "AUTOMOBILE",
            "CONSULTANT"
        ]
    },

    "JD003": {
        "relevant": [
            "INFORMATION-TECHNOLOGY",
            "ENGINEERING"
        ],
        "adjacent": [
            "CONSULTANT",
            "DESIGNER"
        ]
    },

    "JD004": {
        "relevant": [
            "HR"
        ],
        "adjacent": [
            "BUSINESS-DEVELOPMENT",
            "CONSULTANT",
            "PUBLIC-RELATIONS",
            "SALES"
        ]
    },

    "JD005": {
        "relevant": [
            "DIGITAL-MEDIA",
            "PUBLIC-RELATIONS",
            "ARTS"
        ],
        "adjacent": [
            "SALES",
            "BUSINESS-DEVELOPMENT"
        ]
    },

    "JD006": {
        "relevant": [
            "FINANCE",
            "ACCOUNTANT",
            "BANKING"
        ],
        "adjacent": [
            "BUSINESS-DEVELOPMENT",
            "CONSULTANT",
            "INFORMATION-TECHNOLOGY"
        ]
    }
}


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading resumes...")

resumes = pd.read_csv(RESUME_FILE)

jobs = pd.read_csv(JOB_FILE)

print(f"Resumes available: {len(resumes)}")
print(f"Job descriptions: {len(jobs)}")


# ============================================================
# CHECK COLUMNS
# ============================================================

required_resume_columns = {
    "Resume_str",
    "Category"
}

required_job_columns = {
    "job_id",
    "job_title",
    "job_description"
}

missing_resume = (
    required_resume_columns
    - set(resumes.columns)
)

missing_jobs = (
    required_job_columns
    - set(jobs.columns)
)

if missing_resume:
    raise ValueError(
        f"Missing resume columns: {missing_resume}"
    )

if missing_jobs:
    raise ValueError(
        f"Missing job columns: {missing_jobs}"
    )


# ============================================================
# CLEAN RESUME DATA
# ============================================================

resumes = resumes[
    ["Resume_str", "Category"]
].copy()

resumes = resumes.dropna(
    subset=["Resume_str", "Category"]
)

resumes["Resume_str"] = (
    resumes["Resume_str"]
    .astype(str)
    .str.strip()
)

resumes["Category"] = (
    resumes["Category"]
    .astype(str)
    .str.strip()
)


# ============================================================
# GENERATE PAIRS
# ============================================================

all_pairs = []

pair_number = 1


for _, job in jobs.iterrows():

    job_id = job["job_id"]

    print(
        f"\nProcessing {job_id}: "
        f"{job['job_title']}"
    )

    role_config = ROLE_CATEGORIES.get(
        job_id
    )

    if role_config is None:
        raise ValueError(
            f"No category mapping found for {job_id}"
        )

    relevant_categories = (
        role_config["relevant"]
    )

    adjacent_categories = (
        role_config["adjacent"]
    )

    # --------------------------------------------------------
    # Relevant
    # --------------------------------------------------------

    relevant_pool = resumes[
        resumes["Category"].isin(
            relevant_categories
        )
    ]

    relevant_sample = relevant_pool.sample(
        n=min(10, len(relevant_pool)),
        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # Adjacent
    # --------------------------------------------------------

    adjacent_pool = resumes[
        resumes["Category"].isin(
            adjacent_categories
        )
    ]

    adjacent_sample = adjacent_pool.sample(
        n=min(10, len(adjacent_pool)),
        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # Unrelated
    # --------------------------------------------------------

    excluded_categories = (
        set(relevant_categories)
        | set(adjacent_categories)
    )

    unrelated_pool = resumes[
        ~resumes["Category"].isin(
            excluded_categories
        )
    ]

    unrelated_sample = unrelated_pool.sample(
        n=min(10, len(unrelated_pool)),
        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    selected = pd.concat(
        [
            relevant_sample,
            adjacent_sample,
            unrelated_sample
        ]
    )

    # --------------------------------------------------------
    # Create rows
    # --------------------------------------------------------

    for _, resume in selected.iterrows():

        all_pairs.append({

            "pair_id":
                f"P{pair_number:03d}",

            "job_id":
                job_id,

            "job_title":
                job["job_title"],

            "resume_category":
                resume["Category"],

            "resume_text":
                resume["Resume_str"],

            "job_description":
                job["job_description"],

            "human_label":
                "",

            "label_notes":
                ""
        })

        pair_number += 1


# ============================================================
# SAVE
# ============================================================

benchmark = pd.DataFrame(
    all_pairs
)

benchmark.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("COMPATIBILITY BENCHMARK GENERATED")
print("=" * 60)

print(
    f"Total pairs: {len(benchmark)}"
)

print(
    f"Jobs: {benchmark['job_id'].nunique()}"
)

print(
    f"Resume categories: "
    f"{benchmark['resume_category'].nunique()}"
)

print("\nSaved to:")

print(OUTPUT_FILE)

print("=" * 60)