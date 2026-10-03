from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "models/distilbert_resume_model"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading DistilBERT model...")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

print("Model loaded successfully!")
print("Number of labels:", model.config.num_labels)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", device)