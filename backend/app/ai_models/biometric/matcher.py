from sklearn.metrics.pairwise import cosine_similarity

def match_fingerprints(emb1, emb2):
    score = cosine_similarity(emb1, emb2)[0][0]
    return float(score)