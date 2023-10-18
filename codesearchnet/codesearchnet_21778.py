def correlation(a, b):
    """Computes the correlation between a and b, says the Pearson's correlation
    coefficient R
    """
    diff1 = a - a.mean()
    diff2 = b - b.mean()
    return (diff1 * diff2).mean() / (np.sqrt(np.square(diff1).mean() * np.square(diff2).mean()))