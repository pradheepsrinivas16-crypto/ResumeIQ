import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SEMANTIC MATCHING MODEL COMPARISON
# ============================================================

models = pd.DataFrame({
    "Model": [
        "TF-IDF + Cosine",
        "MiniLM + Cosine",
        "BERT + Cosine"
    ],
    "Accuracy": [
        57.50,
        85.00,
        60.00
    ],
    "Spearman": [
        0.8849,
        0.9099,
        0.7079
    ]
})


# Save results
models.to_csv(
    "data/evaluation/semantic_matching_comparison.csv",
    index=False
)


# ============================================================
# ACCURACY GRAPH
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    models["Model"],
    models["Accuracy"]
)

plt.xlabel("Semantic Matching Model")
plt.ylabel("Accuracy (%)")
plt.title("Semantic Matching Model Comparison")

plt.ylim(0, 100)

for i, value in enumerate(models["Accuracy"]):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "data/evaluation/semantic_matching_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# SPEARMAN GRAPH
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    models["Model"],
    models["Spearman"]
)

plt.xlabel("Semantic Matching Model")
plt.ylabel("Spearman Correlation")
plt.title("Semantic Ranking Correlation Comparison")

plt.ylim(0, 1)

for i, value in enumerate(models["Spearman"]):
    plt.text(
        i,
        value + 0.02,
        f"{value:.4f}",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "data/evaluation/semantic_spearman_comparison.png",
    dpi=300
)

plt.close()


print("=" * 60)
print("SEMANTIC MATCHING EVALUATION")
print("=" * 60)

print(models.to_string(index=False))

print("\nFiles created:")
print("data/evaluation/semantic_matching_comparison.csv")
print("data/evaluation/semantic_matching_comparison.png")
print("data/evaluation/semantic_spearman_comparison.png")