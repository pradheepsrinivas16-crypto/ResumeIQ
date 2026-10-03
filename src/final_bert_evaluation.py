import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

INPUT_PATH = "data/evaluation/bert_prediction_check.csv"

CM_PATH = "data/evaluation/bert_confusion_matrix.csv"
REPORT_PATH = "data/evaluation/bert_classification_report.csv"


# Load predictions
df = pd.read_csv(INPUT_PATH)

true_labels = df["true_label"]
predicted_labels = df["predicted_label"]

# Accuracy
accuracy = accuracy_score(true_labels, predicted_labels)

print("=" * 60)
print("FINAL BERT EVALUATION")
print("=" * 60)

print(f"Samples   : {len(df)}")
print(f"Correct   : {df['correct'].sum()}")
print(f"Incorrect : {(~df['correct']).sum()}")
print(f"Accuracy  : {accuracy * 100:.2f}%")

# Classification report
report = classification_report(
    true_labels,
    predicted_labels,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report).transpose()

print("\nClassification Report")
print("=" * 60)
print(report_df)

report_df.to_csv(REPORT_PATH)

# Confusion matrix
labels = sorted(true_labels.unique())

cm = confusion_matrix(
    true_labels,
    predicted_labels,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

cm_df.to_csv(CM_PATH)

print("\nConfusion Matrix")
print("=" * 60)
print(cm_df)

print("\nFiles saved:")
print(REPORT_PATH)
print(CM_PATH)