import pandas as pd
import numpy as np
import torch
import joblib

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score


TEST_PATH = "data/processed/test.csv"
MODEL_PATH = "models/bert_resume_model"
LABEL_ENCODER_PATH = "models/bert_resume_model/label_encoder.pkl"

df = pd.read_csv(TEST_PATH)

texts = df["Resume_str"].fillna("").tolist()
true_labels = df["Category"].tolist()

label_encoder = joblib.load(LABEL_ENCODER_PATH)

true_ids = label_encoder.transform(true_labels)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)
model.eval()

predicted_ids = []

batch_size = 8

for start in range(0, len(texts), batch_size):

    batch = texts[start:start + batch_size]

    inputs = tokenizer(
        batch,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(
        outputs.logits,
        dim=1
    )

    predicted_ids.extend(
        predictions.cpu().numpy()
    )

predicted_ids = np.array(predicted_ids)

accuracy = accuracy_score(
    true_ids,
    predicted_ids
)

print("\n" + "=" * 60)
print("REPRODUCIBILITY CHECK")
print("=" * 60)

print(f"\nSamples      : {len(true_ids)}")
print(f"Correct      : {(true_ids == predicted_ids).sum()}")
print(f"Incorrect    : {(true_ids != predicted_ids).sum()}")
print(f"Accuracy     : {accuracy * 100:.4f}%")

# Save predictions
result = pd.DataFrame({
    "true_label": true_labels,
    "true_id": true_ids,
    "predicted_id": predicted_ids,
    "predicted_label": label_encoder.inverse_transform(predicted_ids),
    "correct": true_ids == predicted_ids
})

output_path = "data/evaluation/bert_prediction_check.csv"

result.to_csv(
    output_path,
    index=False
)

print(f"\nPredictions saved to:")
print(output_path)