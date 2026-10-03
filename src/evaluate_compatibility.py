import os
import sys
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)
from scipy.stats import spearmanr

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)


# ============================================================
# IMPORT SCREENING ENGINE
# ============================================================

from screening_engine import screen_resume


# ============================================================
# PATHS
# ============================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "evaluation",
    "compatibility_test_set.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "evaluation",
    "compatibility_results.csv"
)


# ============================================================
# SCORE → LABEL
# ============================================================

def score_to_label(score):
    """
    Convert compatibility score into an evaluation label.

    These thresholds are used only for this benchmark.
    They should NOT be interpreted as hiring thresholds.
    """

    if score >= 70:
        return "good"

    elif score >= 50:
        return "partial"

    else:
        return "poor"


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("COMPATIBILITY EVALUATION")
print("=" * 60)

print("\nLoading evaluation dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Pairs loaded: {len(df)}")

print("\nHuman labels:")
print(df["label"].value_counts())


# ============================================================
# RUN SCREENING ENGINE
# ============================================================

results = []

print("\nRunning screening engine...")
print("-" * 60)

for index, row in df.iterrows():

    pair_id = row["pair_id"]
    resume_text = row["resume_text"]
    job_description = row["job_description"]
    human_label = row["label"].lower().strip()

    print(
        f"[{index + 1:02d}/{len(df)}] "
        f"Pair {pair_id}..."
    )

    try:

        result = screen_resume(
            resume_text,
            job_description
        )

        semantic_score = float(
            result["semantic_score"]
        )

        skill_score = float(
            result["skill_score"]
        )

        final_score = float(
            result["final_score"]
        )

        predicted_label = score_to_label(
            final_score
        )

        results.append({

            "pair_id": pair_id,

            "human_label": human_label,

            "semantic_score": semantic_score,

            "skill_score": skill_score,

            "final_score": final_score,

            "predicted_label": predicted_label

        })

    except Exception as e:

        print(
            f"ERROR on pair {pair_id}: {e}"
        )

        results.append({

            "pair_id": pair_id,

            "human_label": human_label,

            "semantic_score": None,

            "skill_score": None,

            "final_score": None,

            "predicted_label": "error"

        })


# ============================================================
# CREATE RESULTS DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)

print("\nEvaluation completed.")

# Save raw results
results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nResults saved to:\n{OUTPUT_FILE}"
)


# ============================================================
# REMOVE FAILED PAIRS
# ============================================================

valid_results = results_df[
    results_df["predicted_label"] != "error"
].copy()


# ============================================================
# CLASSIFICATION METRICS
# ============================================================

y_true = valid_results[
    "human_label"
]

y_pred = valid_results[
    "predicted_label"
]


accuracy = accuracy_score(
    y_true,
    y_pred
)

precision, recall, f1, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )
)


print("\n" + "=" * 60)
print("COMPATIBILITY CLASSIFICATION RESULTS")
print("=" * 60)

print(
    f"\nAccuracy          : {accuracy * 100:.2f}%"
)

print(
    f"Weighted Precision: {precision:.4f}"
)

print(
    f"Weighted Recall   : {recall:.4f}"
)

print(
    f"Weighted F1       : {f1:.4f}"
)


# ============================================================
# DETAILED CLASSIFICATION REPORT
# ============================================================

print("\n" + "-" * 60)
print("CLASSIFICATION REPORT")
print("-" * 60)

print(
    classification_report(
        y_true,
        y_pred,
        labels=[
            "good",
            "partial",
            "poor"
        ],
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=[
        "good",
        "partial",
        "poor"
    ]
)

print("-" * 60)
print("CONFUSION MATRIX")
print("-" * 60)

print(
    "\nRows = Human Label"
)

print(
    "Columns = Predicted Label\n"
)

print(
    "             good  partial  poor"
)

for label, row_values in zip(
    ["good", "partial", "poor"],
    cm
):

    print(
        f"{label:<12}"
        f"{row_values[0]:>4}"
        f"{row_values[1]:>9}"
        f"{row_values[2]:>6}"
    )


# ============================================================
# SPEARMAN CORRELATION
# ============================================================

# Convert human labels to an ordered scale.
#
# poor    = 1
# partial = 2
# good    = 3

label_order = {
    "poor": 1,
    "partial": 2,
    "good": 3
}

human_numeric = (
    valid_results["human_label"]
    .map(label_order)
)

system_scores = (
    valid_results["final_score"]
)

spearman_result = spearmanr(
    human_numeric,
    system_scores
)

print("\n" + "-" * 60)
print("RANK CORRELATION")
print("-" * 60)

print(
    f"\nSpearman correlation: "
    f"{spearman_result.statistic:.4f}"
)

print(
    f"P-value            : "
    f"{spearman_result.pvalue:.6f}"
)


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

print("\n" + "-" * 60)
print("AVERAGE SCORES BY HUMAN LABEL")
print("-" * 60)

score_summary = (
    valid_results
    .groupby("human_label")[
        [
            "semantic_score",
            "skill_score",
            "final_score"
        ]
    ]
    .mean()
    .reindex(
        ["good", "partial", "poor"]
    )
)

print(
    score_summary.round(2)
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)

print(
    f"""
Evaluation pairs : {len(valid_results)}
Accuracy          : {accuracy * 100:.2f}%
Weighted F1       : {f1:.4f}
Spearman          : {spearman_result.statistic:.4f}
"""
)

print("=" * 60)
print("DONE")
print("=" * 60)