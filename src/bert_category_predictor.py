import os
import sys
import joblib
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --------------------------------------------------
# PATHS
# --------------------------------------------------

MODEL_PATH = os.path.join("models", "bert_resume_model")


# --------------------------------------------------
# LOAD BERT
# --------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()

label_encoder = joblib.load(
    os.path.join(MODEL_PATH, "label_encoder.pkl")
)


# --------------------------------------------------
# PREDICT TOP CATEGORIES
# --------------------------------------------------

def predict_top_categories(resume_text, top_k=3):

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
        )[0]

    top_probabilities, top_indices = torch.topk(
        probabilities,
        k=top_k
    )

    results = []

    for probability, index in zip(
        top_probabilities,
        top_indices
    ):

        category = label_encoder.inverse_transform(
            [index.item()]
        )[0]

        confidence = probability.item() * 100

        results.append({
            "category": category,
            "confidence": round(confidence, 2)
        })

    return results


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "\nUsage:"
        )

        print(
            "python src/bert_category_predictor.py <resume_file>"
        )

        print(
            "\nExample:"
        )

        print(
            "python src/bert_category_predictor.py resume.pdf"
        )

        sys.exit()

    resume_file = sys.argv[1]

    # Import parser only when needed
    from resume_parser import extract_resume_text

    print("\nReading resume...")

    resume_text = extract_resume_text(resume_file)

    if not resume_text.strip():

        print("ERROR: Could not extract resume text.")

        sys.exit()

    print(
        f"Extracted {len(resume_text)} characters."
    )

    print("\nRunning BERT classification...")

    predictions = predict_top_categories(
        resume_text,
        top_k=3
    )

    print("\n" + "=" * 50)
    print("BERT TOP 3 RESUME CATEGORIES")
    print("=" * 50)

    for i, prediction in enumerate(
        predictions,
        start=1
    ):

        print(
            f"{i}. "
            f"{prediction['category']} "
            f"— "
            f"{prediction['confidence']:.2f}%"
        )

    print("=" * 50)