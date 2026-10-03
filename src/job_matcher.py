from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load Sentence Transformer model
MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading Sentence Transformer...")

model = SentenceTransformer(MODEL_NAME)

print("Sentence Transformer loaded!")


def calculate_match_score(resume_text, job_description):
    """
    Calculate semantic similarity between a resume
    and a job description.
    """

    # Convert resume and job description into embeddings
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    # Convert similarity to percentage
    match_score = similarity * 100

    return match_score