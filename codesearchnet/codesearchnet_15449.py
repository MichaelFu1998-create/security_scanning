def count_cycles(series, ndigits=None, left=False, right=False):
    """Count cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers
    ndigits : int, optional
        Round cycle magnitudes to the given number of digits before counting.
    left: bool, optional
        If True, treat the first point in the series as a reversal.
    right: bool, optional
        If True, treat the last point in the series as a reversal.

    Returns
    -------
    A sorted list containing pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers.
    """
    counts = defaultdict(float)
    round_ = _get_round_function(ndigits)

    for low, high, mult in extract_cycles(series, left=left, right=right):
        delta = round_(abs(high - low))
        counts[delta] += mult
    return sorted(counts.items())