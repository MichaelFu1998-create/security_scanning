def round_any(x, accuracy, f=np.round):
    """
    Round to multiple of any number.
    """
    if not hasattr(x, 'dtype'):
        x = np.asarray(x)

    return f(x / accuracy) * accuracy