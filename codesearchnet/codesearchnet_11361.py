def pylint_color(score):
    """Return Pylint badge color.

    Parameters
    ----------
    score : float
        A Pylint score

    Returns
    -------
    str
        Badge color

    """
    # These are the score cutoffs for each color above.
    # I.e. score==10 -> brightgreen, down to 7.5 > score >= 5 -> orange
    score_cutoffs = (10, 9.5, 8.5, 7.5, 5)
    for i in range(len(score_cutoffs)):
        if score >= score_cutoffs[i]:
            return BADGE_COLORS[i]
    # and score < 5 -> red
    return BADGE_COLORS[-1]