def fmt(a, b):
    """Figure of merit in time
    """
    return 100 * np.min([a, b], axis=0).sum() / np.max([a, b], axis=0).sum()