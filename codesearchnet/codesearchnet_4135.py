def histogram(ratings, min_rating=None, max_rating=None):
    """
    Generates a frequency count of each rating on the scale
    ratings is a list of scores
    Returns a list of frequencies
    """
    ratings = [int(r) for r in ratings]
    if min_rating is None:
        min_rating = min(ratings)
    if max_rating is None:
        max_rating = max(ratings)
    num_ratings = int(max_rating - min_rating + 1)
    hist_ratings = [0 for x in range(num_ratings)]
    for r in ratings:
        hist_ratings[r - min_rating] += 1
    return hist_ratings