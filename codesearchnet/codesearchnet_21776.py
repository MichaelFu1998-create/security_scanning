def fa(a, b, alpha=2):
    """Returns the factor of 'alpha' (2 or 5 normally)
    """
    return np.sum((a > b / alpha) & (a < b * alpha), dtype=float) / len(a) * 100