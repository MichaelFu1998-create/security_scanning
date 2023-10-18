def gmb(a, b):
    """Geometric mean bias
    """
    return np.exp(np.log(a).mean() - np.log(b).mean())