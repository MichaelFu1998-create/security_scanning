def confusion_matrix(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Generates a confusion matrix between rater_a and rater_b
    A confusion matrix shows how often 2 values agree and disagree
    See quadratic_weighted_kappa for argument descriptions
    """
    assert(len(rater_a) == len(rater_b))
    rater_a = [int(a) for a in rater_a]
    rater_b = [int(b) for b in rater_b]
    min_rating = int(min_rating)
    max_rating = int(max_rating)
    if min_rating is None:
        min_rating = min(rater_a)
    if max_rating is None:
        max_rating = max(rater_a)
    num_ratings = int(max_rating - min_rating + 1)
    conf_mat = [[0 for i in range(num_ratings)]
                for j in range(num_ratings)]
    for a, b in zip(rater_a, rater_b):
        conf_mat[int(a - min_rating)][int(b - min_rating)] += 1
    return conf_mat