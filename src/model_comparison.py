import pandas as pd


results = {
    "Model": [
        "TF-IDF + SVM",
        "Sentence Transformer + SVM",
        "CNN",
        "LSTM",
        "DistilBERT"
    ],

    "Test Accuracy": [
        72.12,
        74.80,
        67.83,
        10.72,
        80.43
    ],

    "Weighted F1": [
        0.71,
        0.73,
        0.64,
        0.10,
        None
    ]
}


df = pd.DataFrame(results)


print("\n==============================================")
print("          MODEL COMPARISON")
print("==============================================")

print(df.to_string(index=False))

print("\n==============================================")
print("       EXPERIMENT SUMMARY")
print("==============================================")

print("Highest tested accuracy: DistilBERT - 80.43%")
print("CNN accuracy: 67.83%")
print("LSTM accuracy: 10.72%")

print("==============================================")


# Save results
df.to_csv(
    "data/processed/model_comparison.csv",
    index=False
)

print("\nSaved to:")
print("data/processed/model_comparison.csv")