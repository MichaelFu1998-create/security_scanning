def quadratic_weighted_kappa(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Calculates kappa correlation between rater_a and rater_b.
    Kappa measures how well 2 quantities vary together.
    rater_a is a list of rater a scores
    rater_b is a list of rater b scores
    min_rating is an optional argument describing the minimum rating possible on the data set
    max_rating is an optional argument describing the maximum rating possible on the data set
    Returns a float corresponding to the kappa correlation
    """
    assert(len(rater_a) == len(rater_b))
    rater_a = [int(a) for a in rater_a]
    rater_b = [int(b) for b in rater_b]
    if min_rating is None:
        min_rating = min(rater_a + rater_b)
    if max_rating is None:
        max_rating = max(rater_a + rater_b)
    conf_mat = confusion_matrix(rater_a, rater_b,
        min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    if(num_ratings > 1):
        for i in range(num_ratings):
            for j in range(num_ratings):
                expected_count = (hist_rater_a[i] * hist_rater_b[j]
                                  / num_scored_items)
                d = pow(i - j, 2.0) / pow(num_ratings - 1, 2.0)
                numerator += d * conf_mat[i][j] / num_scored_items
                denominator += d * expected_count / num_scored_items

        return 1.0 - numerator / denominator
    else:
        return 1.0