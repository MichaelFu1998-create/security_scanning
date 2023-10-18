def nearest_int(x):
    """
    Return nearest long integer to x
    """
    if x == 0:
        return np.int64(0)
    elif x > 0:
        return np.int64(x + 0.5)
    else:
        return np.int64(x - 0.5)