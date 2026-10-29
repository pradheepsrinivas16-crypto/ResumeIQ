import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Lazy load model
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def calibrate_semantic_score(raw_cosine):
    """
    MiniLM cosine similarity between a detailed resume and JD typically ranges 
    between 0.20 (irrelevant) and 0.55 (near-perfect domain fit).
    This calibrated mapping scales 0.15–0.60 to a natural 10%–95% ATS range.
    """
    if raw_cosine <= 0.15:
        scaled = max(0.0, raw_cosine * 100 * 0.5)
    elif raw_cosine < 0.30:
        # 0.15 to 0.30 -> 15% to 45%
        scaled = 15.0 + ((raw_cosine - 0.15) / 0.15) * 30.0
    elif raw_cosine < 0.45:
        # 0.30 to 0.45 -> 45% to 75%
        scaled = 45.0 + ((raw_cosine - 0.30) / 0.15) * 30.0
    else:
        # 0.45 to 0.65 -> 75% to 95%
        scaled = 75.0 + min(20.0, ((raw_cosine - 0.45) / 0.20) * 20.0)
    
    return float(np.clip(scaled, 0.0, 100.0))

def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0

    model = get_model()
    embeddings = model.encode([resume_text, job_description])
    raw_similarity = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

    return round(calibrate_semantic_score(raw_similarity), 1)