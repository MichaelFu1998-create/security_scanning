def cosine(vec1, vec2):
    """Compare vectors. Borrowed from A. Parish."""
    if norm(vec1) > 0 and norm(vec2) > 0:
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    else:
        return 0.0