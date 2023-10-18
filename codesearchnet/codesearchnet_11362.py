def pydocstyle_color(score):
    """Return pydocstyle badge color.

    Parameters
    ----------
    score : float
        A pydocstyle score

    Returns
    -------
    str
        Badge color

    """
    # These are the score cutoffs for each color above.
    # I.e. score==0 -> brightgreen, down to 100 < score <= 200 -> orange
    score_cutoffs = (0, 10, 25, 50, 100)
    for i in range(len(score_cutoffs)):
        if score <= score_cutoffs[i]:
            return BADGE_COLORS[i]
    # and score > 200 -> red
    return BADGE_COLORS[-1]