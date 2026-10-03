import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# -----------------------------------------
# Model path
# -----------------------------------------

MODEL_PATH = "models/distilbert_resume_model"


# -----------------------------------------
# Resume categories
# -----------------------------------------

CATEGORIES = [
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
# Load model
# -----------------------------------------

print("Loading DistilBERT category model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)
model.eval()

print("DistilBERT category model loaded!")


# -----------------------------------------
# Predict category
# -----------------------------------------

def predict_category(resume_text):
    """
    Predict the category of a resume.
    """

    inputs = tokenizer(
        resume_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )

    predicted_class = torch.argmax(
        probabilities,
        dim=1
    ).item()

    confidence = (
        probabilities[0][predicted_class].item()
        * 100
    )

    category = CATEGORIES[predicted_class]

    return category, confidence