def rmse(a, b):
    """Returns the root mean square error betwwen a and b
    """
    return np.sqrt(np.square(a - b).mean())