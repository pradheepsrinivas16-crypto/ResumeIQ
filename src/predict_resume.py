from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from resume_parser import extract_resume_text


# -----------------------------------------
# 1. Paths
# -----------------------------------------

MODEL_PATH = "models/distilbert_resume_model"
RESUME_PATH = "Pradeep_Srinivas_Resume_ATS (1).pdf"


# -----------------------------------------
# 2. Category mapping
# -----------------------------------------

categories = [
    "ACCOUNTANT",
    "ADVOCATE",
    "AGRICULTURE",
    "APPAREL",
    "ARTS",
    "AUTOMOBILE",
    "AVIATION",
    "BANKING",
    "BPO",
    "BUSINESS-DEVELOPMENT",
    "CHEF",
    "CONSTRUCTION",
    "CONSULTANT",
    "DESIGNER",
    "DIGITAL-MEDIA",
    "ENGINEERING",
    "FINANCE",
    "FITNESS",
    "HEALTHCARE",
    "HR",
    "INFORMATION-TECHNOLOGY",
    "PUBLIC-RELATIONS",
    "SALES",
    "TEACHER"
]


# -----------------------------------------
# 3. Load model and tokenizer
# -----------------------------------------

print("Loading DistilBERT model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)
model.eval()

print("Model loaded!")
print("Device:", device)


# -----------------------------------------
# 4. Extract resume text
# -----------------------------------------

print("\nReading resume...")

resume_text = extract_resume_text(RESUME_PATH)

print("Resume extracted!")
print("Characters:", len(resume_text))


# -----------------------------------------
# 5. Tokenize resume
# -----------------------------------------

inputs = tokenizer(
    resume_text,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=256
)

# Move inputs to same device as model
inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}


# -----------------------------------------
# 6. Predict
# -----------------------------------------

print("\nPredicting resume category...")

with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits

predicted_class = torch.argmax(logits, dim=1).item()

predicted_category = categories[predicted_class]


# -----------------------------------------
# 7. Confidence
# -----------------------------------------

probabilities = torch.softmax(logits, dim=1)

confidence = probabilities[0][predicted_class].item() * 100


# -----------------------------------------
# 8. Display result
# -----------------------------------------

print("\n======================================")
print("       RESUME SCREENING RESULT")
print("======================================")

print("Predicted Category:", predicted_category)
print(f"Model Confidence: {confidence:.2f}%")

print("======================================")