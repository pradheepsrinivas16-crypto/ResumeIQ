import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


# ============================================================
# 1. MODEL COMPARISON
# ============================================================

models = pd.DataFrame({
    "Model": [
        "TF-IDF + SVM",
        "Sentence Transformer + SVM",
        "CNN",
        "LSTM",
        "BERT"
    ],
    "Accuracy": [
        72.12,
        74.80,
        67.83,
        10.72,
        79.36
    ],
    "Weighted_F1": [
        71.00,
        73.00,
        64.00,
        10.00,
        77.38
    ]
})

models.to_csv(
    "data/evaluation/final_model_comparison.csv",
    index=False
)


# ============================================================
# 2. ACCURACY GRAPH
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    models["Model"],
    models["Accuracy"]
)

plt.ylabel("Test Accuracy (%)")
plt.xlabel("Model")
plt.title("Resume Classification Model Comparison")

plt.xticks(rotation=20)
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
    "data/evaluation/model_accuracy_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. BERT CONFUSION MATRIX
# ============================================================

cm = pd.read_csv(
    "data/evaluation/bert_confusion_matrix.csv",
    index_col=0
)

fig, ax = plt.subplots(figsize=(14, 12))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm.values,
    display_labels=cm.index
)

disp.plot(
    ax=ax,
    xticks_rotation=90,
    cmap="Blues",
    colorbar=True
)

plt.title("BERT Resume Classification Confusion Matrix")

plt.tight_layout()

plt.savefig(
    "data/evaluation/bert_confusion_matrix_final.png",
    dpi=300
)

plt.close()


print("=" * 60)
print("FINAL EVALUATION FILES CREATED")
print("=" * 60)

print("\nModel comparison:")
print(models)

print("\nFiles created:")

print("data/evaluation/final_model_comparison.csv")
print("data/evaluation/model_accuracy_comparison.png")
print("data/evaluation/bert_confusion_matrix_final.png")