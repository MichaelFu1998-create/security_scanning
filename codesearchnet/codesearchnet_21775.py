def mfbe(a, b):
    """Returns the mean fractionalized bias error
    """
    return 2 * bias(a, b) / (a.mean() + b.mean())