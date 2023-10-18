def gmv(a, b):
    """Geometric mean variance
    """
    return np.exp(np.square(np.log(a) - np.log(b)).mean())