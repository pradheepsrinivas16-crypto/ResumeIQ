import pandas as pd
import matplotlib.pyplot as plt

# Load model results
df = pd.read_csv(
    "data/processed/model_comparison.csv"
)

# Create accuracy chart
plt.figure(figsize=(10, 6))

plt.bar(
    df["Model"],
    df["Test Accuracy"]
)

plt.title("Resume Classification Model Comparison")
plt.xlabel("Model")
plt.ylabel("Test Accuracy (%)")

plt.xticks(
    rotation=25,
    ha="right"
)

plt.ylim(0, 100)

plt.tight_layout()

# Save chart
plt.savefig(
    "data/processed/model_accuracy_comparison.png",
    dpi=300
)

plt.show()

print("\nChart saved successfully:")
print(
    "data/processed/model_accuracy_comparison.png"
)