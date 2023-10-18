def sample_top(a=None, top_k=10):
    """Sample from ``top_k`` probabilities.

    Parameters
    ----------
    a : list of float
        List of probabilities.
    top_k : int
        Number of candidates to be considered.

    """
    if a is None:
        a = []

    idx = np.argpartition(a, -top_k)[-top_k:]
    probs = a[idx]
    # tl.logging.info("new %f" % probs)
    probs = probs / np.sum(probs)
    choice = np.random.choice(idx, p=probs)
    return choice