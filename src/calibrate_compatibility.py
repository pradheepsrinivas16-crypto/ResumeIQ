import pandas as pd
import numpy as np
from scipy.stats import spearmanr


RESULTS_PATH = "data/evaluation/compatibility_results.csv"


# ---------------------------------------------------------
# LOAD RESULTS
# ---------------------------------------------------------

df = pd.read_csv(RESULTS_PATH)

print("\n" + "=" * 70)
print("COMPATIBILITY SCORE CALIBRATION ANALYSIS")
print("=" * 70)

print(f"\nTotal evaluation pairs: {len(df)}")


# ---------------------------------------------------------
# SCORE DISTRIBUTION
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("SCORE DISTRIBUTION BY HUMAN LABEL")
print("-" * 70)

summary = (
    df.groupby("human_label")["final_score"]
    .agg(["count", "min", "max", "mean", "median", "std"])
)

print(summary)


# ---------------------------------------------------------
# SORT SCORES
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("ALL SCORES — LOW TO HIGH")
print("-" * 70)

sorted_df = df[
    ["pair_id", "human_label", "final_score", "predicted_label"]
].sort_values("final_score")

print(sorted_df.to_string(index=False))


# ---------------------------------------------------------
# SIMPLE NORMALIZATION
# ---------------------------------------------------------

min_score = df["final_score"].min()
max_score = df["final_score"].max()

df["normalized_score"] = (
    (df["final_score"] - min_score)
    / (max_score - min_score)
    * 100
)

print("\n" + "-" * 70)
print("NORMALIZED 0–100 SCORE")
print("-" * 70)

print(
    df[
        ["pair_id", "human_label", "final_score", "normalized_score"]
    ]
    .sort_values("normalized_score", ascending=False)
    .to_string(index=False)
)


# ---------------------------------------------------------
# RANK CORRELATION
# ---------------------------------------------------------

label_mapping = {
    "poor": 1,
    "partial": 2,
    "good": 3
}

human_numeric = df["human_label"].map(label_mapping)

raw_corr, raw_p = spearmanr(
    df["final_score"],
    human_numeric
)

normalized_corr, normalized_p = spearmanr(
    df["normalized_score"],
    human_numeric
)

print("\n" + "-" * 70)
print("RANK CORRELATION")
print("-" * 70)

print(f"Raw score Spearman        : {raw_corr:.4f}")
print(f"Normalized score Spearman : {normalized_corr:.4f}")


# ---------------------------------------------------------
# RANGE ANALYSIS
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("CLASS RANGES")
print("-" * 70)

for label in ["poor", "partial", "good"]:

    scores = df.loc[
        df["human_label"] == label,
        "final_score"
    ]

    print(
        f"{label:8s} : "
        f"{scores.min():8.2f} → {scores.max():8.2f}"
    )


# ---------------------------------------------------------
# OVERLAP ANALYSIS
# ---------------------------------------------------------

poor_max = df.loc[
    df["human_label"] == "poor",
    "final_score"
].max()

partial_min = df.loc[
    df["human_label"] == "partial",
    "final_score"
].min()

partial_max = df.loc[
    df["human_label"] == "partial",
    "final_score"
].max()

good_min = df.loc[
    df["human_label"] == "good",
    "final_score"
].min()
    
print("\n" + "-" * 70)
print("CLASS OVERLAP")
print("-" * 70)

print(f"Poor maximum     : {poor_max:.2f}")
print(f"Partial minimum  : {partial_min:.2f}")
print(f"Partial maximum  : {partial_max:.2f}")
print(f"Good minimum     : {good_min:.2f}")


# ---------------------------------------------------------
# FINAL OBSERVATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("CALIBRATION ANALYSIS COMPLETE")
print("=" * 70)

print("""
This experiment does NOT modify the production scoring system.

It only studies whether the existing compatibility scores
can reasonably be transformed into a user-facing 0–100 score.

The original Experiment 1 results remain unchanged.
""")