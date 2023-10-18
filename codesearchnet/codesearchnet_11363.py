def flake8_color(score):
    """Return flake8 badge color.

    Parameters
    ----------
    score : float
        A flake8 score

    Returns
    -------
    str
        Badge color

    """
    # These are the score cutoffs for each color above.
    # I.e. score==0 -> brightgreen, down to 100 < score <= 200 -> orange
    score_cutoffs = (0, 20, 50, 100, 200)
    for i in range(len(score_cutoffs)):
        if score <= score_cutoffs[i]:
            return BADGE_COLORS[i]
    # and score > 200 -> red
    return BADGE_COLORS[-1]