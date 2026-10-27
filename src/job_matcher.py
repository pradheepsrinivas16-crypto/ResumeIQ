import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


@st.cache_resource
def get_sentence_transformer():
    return SentenceTransformer(MODEL_NAME)


def calculate_match_score(resume_text, job_description):
    """
    Calculate semantic similarity between a resume
    and a job description.
    """

    # Convert resume and job description into embeddings
    model = get_sentence_transformer()
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