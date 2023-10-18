def nmse(a, b):
    """Returns the normalized mean square error of a and b
    """
    return np.square(a - b).mean() / (a.mean() * b.mean())