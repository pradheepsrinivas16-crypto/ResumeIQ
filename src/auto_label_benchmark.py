import pandas as pd
from pathlib import Path

from job_matcher import calculate_match_score
from skill_matcher import compare_skills


INPUT_FILE = Path("data/evaluation/compatibility_benchmark_raw.csv")
OUTPUT_FILE = Path("data/evaluation/compatibility_benchmark_labeled.csv")


def calculate_skill_score(matched_skills, required_skills):
    if not required_skills:
        return 0.0

    return len(matched_skills) / len(required_skills) * 100


def preliminary_label(semantic_score, skill_score):
    """
    Preliminary heuristic label.

    Good:
        Strong semantic alignment AND strong skill coverage

    Partial:
        Moderate alignment or mixed evidence

    Poor:
        Low semantic alignment AND very low skill coverage
    """

    if semantic_score >= 70 and skill_score >= 70:
        return "good"

    if semantic_score < 40 and skill_score < 30:
        return "poor"

    return "partial"


def main():

    print("Loading benchmark...")

    df = pd.read_csv(INPUT_FILE)

    results = []

    for index, row in df.iterrows():

        resume_text = str(row["resume_text"])
        job_description = str(row["job_description"])

        print(
            f"Processing {row['pair_id']} "
            f"({index + 1}/{len(df)})"
        )

        # Semantic similarity
        semantic_score = calculate_match_score(
            resume_text,
            job_description
        )

        # Skill matching
        skill_result = compare_skills(
            resume_text,
            job_description
        )

        skill_score = calculate_skill_score(
            skill_result["matched_skills"],
            skill_result["required_skills"]
        )

        label = preliminary_label(
            semantic_score,
            skill_score
        )

        results.append({
            "pair_id": row["pair_id"],
            "job_id": row["job_id"],
            "job_title": row["job_title"],
            "resume_category": row["resume_category"],
            "semantic_score": round(semantic_score, 2),
            "skill_score": round(skill_score, 2),
            "preliminary_label": label
        })

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("AUTOMATIC BENCHMARK LABELING COMPLETE")
    print("=" * 60)

    print("\nLabel distribution:")
    print(result_df["preliminary_label"].value_counts())

    print("\nAverage scores:")
    print(
        result_df.groupby("preliminary_label")[
            ["semantic_score", "skill_score"]
        ].mean()
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()