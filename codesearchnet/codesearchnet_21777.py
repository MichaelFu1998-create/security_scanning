def foex(a, b):
    """Returns the factor of exceedance
    """
    return (np.sum(a > b, dtype=float) / len(a) - 0.5) * 100