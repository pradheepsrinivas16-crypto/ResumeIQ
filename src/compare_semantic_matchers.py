import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr

from sentence_transformers import SentenceTransformer

import torch
from transformers import AutoTokenizer, AutoModel


# =========================================================
# PATHS
# =========================================================

DATASET_PATH = "data/evaluation/compatibility_test_set.csv"

BERT_MODEL_PATH = "models/bert_resume_model"


# =========================================================
# LOAD DATA
# =========================================================

print("\n" + "=" * 70)
print("SEMANTIC MATCHING MODEL COMPARISON")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(f"\nEvaluation pairs: {len(df)}")


# =========================================================
# TEXT
# =========================================================

resumes = df["resume_text"].fillna("").tolist()
jobs = df["job_description"].fillna("").tolist()


# =========================================================
# HUMAN LABELS
# =========================================================

label_mapping = {
    "poor": 1,
    "partial": 2,
    "good": 3
}

human_labels = df["label"].map(label_mapping)


# =========================================================
# 1. TF-IDF COSINE
# =========================================================

print("\n" + "-" * 70)
print("1. TF-IDF + COSINE")
print("-" * 70)

all_text = resumes + jobs

tfidf = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=10000
)

tfidf_matrix = tfidf.fit_transform(all_text)

resume_vectors = tfidf_matrix[:len(resumes)]
job_vectors = tfidf_matrix[len(resumes):]

tfidf_scores = []

for i in range(len(df)):

    similarity = cosine_similarity(
        resume_vectors[i],
        job_vectors[i]
    )[0][0]

    tfidf_scores.append(similarity * 100)

tfidf_scores = np.array(tfidf_scores)

print("TF-IDF matching completed.")


# =========================================================
# 2. MINILM COSINE
# =========================================================

print("\n" + "-" * 70)
print("2. MiniLM + COSINE")
print("-" * 70)

print("Loading MiniLM...")

minilm = SentenceTransformer("all-MiniLM-L6-v2")

resume_embeddings = minilm.encode(
    resumes,
    convert_to_numpy=True,
    show_progress_bar=True
)

job_embeddings = minilm.encode(
    jobs,
    convert_to_numpy=True,
    show_progress_bar=True
)

minilm_scores = []

for i in range(len(df)):

    similarity = cosine_similarity(
        resume_embeddings[i].reshape(1, -1),
        job_embeddings[i].reshape(1, -1)
    )[0][0]

    minilm_scores.append(similarity * 100)

minilm_scores = np.array(minilm_scores)

print("MiniLM matching completed.")


# =========================================================
# 3. BERT COSINE
# =========================================================

print("\n" + "-" * 70)
print("3. BERT + COSINE")
print("-" * 70)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(
    BERT_MODEL_PATH
)

bert = AutoModel.from_pretrained(
    BERT_MODEL_PATH
)

bert.to(device)
bert.eval()


def get_bert_embedding(text):

    inputs = tokenizer(
        text,
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

        outputs = bert(**inputs)

    # Mean pooling
    hidden_states = outputs.last_hidden_state

    attention_mask = inputs["attention_mask"]

    mask = attention_mask.unsqueeze(-1).expand(
        hidden_states.size()
    ).float()

    summed = torch.sum(
        hidden_states * mask,
        dim=1
    )

    counts = torch.clamp(
        mask.sum(dim=1),
        min=1e-9
    )

    embedding = summed / counts

    return embedding.cpu().numpy()[0]


print("Encoding resumes...")

bert_resume_embeddings = np.array([
    get_bert_embedding(text)
    for text in resumes
])

print("Encoding job descriptions...")

bert_job_embeddings = np.array([
    get_bert_embedding(text)
    for text in jobs
])


bert_scores = []

for i in range(len(df)):

    similarity = cosine_similarity(
        bert_resume_embeddings[i].reshape(1, -1),
        bert_job_embeddings[i].reshape(1, -1)
    )[0][0]

    bert_scores.append(similarity * 100)

bert_scores = np.array(bert_scores)

print("BERT matching completed.")


# =========================================================
# RESULTS TABLE
# =========================================================
results = pd.DataFrame({
    "pair_id": df["pair_id"],
    "human_label": df["label"],
    "tfidf_score": tfidf_scores,
    "minilm_score": minilm_scores,
    "bert_score": bert_scores
})


# =========================================================
# SPEARMAN
# =========================================================

tfidf_corr, tfidf_p = spearmanr(
    tfidf_scores,
    human_labels
)

minilm_corr, minilm_p = spearmanr(
    minilm_scores,
    human_labels
)

bert_corr, bert_p = spearmanr(
    bert_scores,
    human_labels
)


# =========================================================
# THRESHOLD CLASSIFICATION
# =========================================================

def classify(score):

    if score >= 70:
        return "good"

    elif score >= 50:
        return "partial"

    else:
        return "poor"


results["tfidf_prediction"] = results["tfidf_score"].apply(classify)
results["minilm_prediction"] = results["minilm_score"].apply(classify)
results["bert_prediction"] = results["bert_score"].apply(classify)


tfidf_accuracy = (
    results["tfidf_prediction"] == results["human_label"]
).mean()

minilm_accuracy = (
    results["minilm_prediction"] == results["human_label"]
).mean()

bert_accuracy = (
    results["bert_prediction"] == results["human_label"]
).mean()


# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("SEMANTIC MATCHING COMPARISON")
print("=" * 70)

print(
    f"\n{'Model':<25}"
    f"{'Accuracy':>12}"
    f"{'Spearman':>12}"
)

print("-" * 50)

print(
    f"{'TF-IDF + Cosine':<25}"
    f"{tfidf_accuracy * 100:>11.2f}%"
    f"{tfidf_corr:>12.4f}"
)

print(
    f"{'MiniLM + Cosine':<25}"
    f"{minilm_accuracy * 100:>11.2f}%"
    f"{minilm_corr:>12.4f}"
)

print(
    f"{'BERT + Cosine':<25}"
    f"{bert_accuracy * 100:>11.2f}%"
    f"{bert_corr:>12.4f}"
)


# =========================================================
# AVERAGE SCORE BY HUMAN LABEL
# =========================================================

print("\n" + "-" * 70)
print("AVERAGE SCORE BY HUMAN LABEL")
print("-" * 70)

average_scores = results.groupby("human_label")[
    ["tfidf_score", "minilm_score", "bert_score"]
].mean()

print(average_scores)


# =========================================================
# SAVE RESULTS
# =========================================================

output_path = "data/evaluation/semantic_matcher_comparison.csv"

results.to_csv(
    output_path,
    index=False
)

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)