def weighted_mode(values, weights):
    """Return the value with the greatest total weight.
    >>> weighted_mode('abbaa', [1,2,3,1,2])
    'b'"""
    totals = defaultdict(int)
    for v, w in zip(values, weights):
        totals[v] += w
    return max(totals.keys(), key=totals.get)