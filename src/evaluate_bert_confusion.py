import os
import joblib
import numpy as np
import pandas as pd
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# =========================================================
# PATHS
# =========================================================

TEST_PATH = "data/processed/test.csv"
MODEL_PATH = "models/bert_resume_model"
LABEL_ENCODER_PATH = "models/bert_resume_model/label_encoder.pkl"

OUTPUT_DIR = "data/evaluation"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# DEVICE
# =========================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("\n" + "=" * 70)
print("BERT CLASSIFICATION EVALUATION")
print("=" * 70)

print(f"\nUsing device: {device}")


# =========================================================
# LOAD TEST DATA
# =========================================================

print("\nLoading test dataset...")

df = pd.read_csv(TEST_PATH)

texts = df["Resume_str"].fillna("").tolist()
true_labels = df["Category"].tolist()

print(f"Test samples: {len(df)}")


# =========================================================
# LOAD LABEL ENCODER
# =========================================================

label_encoder = joblib.load(LABEL_ENCODER_PATH)

class_names = label_encoder.classes_

print(f"Number of classes: {len(class_names)}")


# =========================================================
# LOAD BERT
# =========================================================

print("\nLoading BERT model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()

print("BERT model loaded successfully.")


# =========================================================
# PREDICTIONS
# =========================================================

print("\nGenerating predictions...")

predicted_ids = []

batch_size = 8

for start in range(0, len(texts), batch_size):

    batch_texts = texts[start:start + batch_size]

    inputs = tokenizer(
        batch_texts,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model(**inputs)

    predictions = torch.argmax(
        outputs.logits,
        dim=1
    )

    predicted_ids.extend(
        predictions.cpu().numpy().tolist()
    )

    print(
        f"[{min(start + batch_size, len(texts))}/{len(texts)}]"
    )


# =========================================================
# CONVERT LABELS
# =========================================================

true_ids = label_encoder.transform(true_labels)

predicted_labels = label_encoder.inverse_transform(
    predicted_ids
)


# =========================================================
# ACCURACY
# =========================================================

accuracy = accuracy_score(
    true_ids,
    predicted_ids
)

print("\n" + "=" * 70)
print("BERT TEST RESULTS")
print("=" * 70)

print(f"\nAccuracy : {accuracy * 100:.2f}%")


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

report = classification_report(
    true_ids,
    predicted_ids,
    target_names=class_names,
    zero_division=0
)

print("\n" + "-" * 70)
print("CLASSIFICATION REPORT")
print("-" * 70)

print(report)


# =========================================================
# SAVE CLASSIFICATION REPORT
# =========================================================

report_dict = classification_report(
    true_ids,
    predicted_ids,
    target_names=class_names,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report_dict).transpose()

report_path = (
    f"{OUTPUT_DIR}/bert_classification_report.csv"
)

report_df.to_csv(report_path)

print(f"Classification report saved to:")
print(report_path)


# =========================================================
# CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(
    true_ids,
    predicted_ids
)

print("\n" + "-" * 70)
print("CONFUSION MATRIX")
print("-" * 70)

print(cm)


# =========================================================
# SAVE CONFUSION MATRIX
# =========================================================

cm_df = pd.DataFrame(
    cm,
    index=class_names,
    columns=class_names
)

cm_path = (
    f"{OUTPUT_DIR}/bert_confusion_matrix.csv"
)

cm_df.to_csv(cm_path)

print(f"\nConfusion matrix saved to:")
print(cm_path)


# =========================================================
# PLOT CONFUSION MATRIX
# =========================================================

fig, ax = plt.subplots(
    figsize=(18, 16)
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

display.plot(
    ax=ax,
    xticks_rotation=90,
    cmap="Blues",
    values_format="d"
)

plt.title(
    "BERT Resume Classification - Confusion Matrix"
)

plt.tight_layout()

plot_path = (
    f"{OUTPUT_DIR}/bert_confusion_matrix.png"
)

plt.savefig(
    plot_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Confusion matrix image saved to:")
print(plot_path)


# =========================================================
# TOP CONFUSIONS
# =========================================================

print("\n" + "-" * 70)
print("TOP CONFUSIONS")
print("-" * 70)

confusions = []

for i in range(len(class_names)):

    for j in range(len(class_names)):

        if i != j and cm[i][j] > 0:

            confusions.append(
                (
                    cm[i][j],
                    class_names[i],
                    class_names[j]
                )
            )

confusions.sort(
    reverse=True
)

if confusions:

    for count, actual, predicted in confusions[:15]:

        print(
            f"{actual} → {predicted}: {count}"
        )

else:

    print("No classification errors.")


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)