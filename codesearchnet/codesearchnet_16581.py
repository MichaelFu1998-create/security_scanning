def _distances(value_domain, distance_metric, n_v):
    """Distances of the different possible values.

    Parameters
    ----------
    value_domain : array_like, with shape (V,)
        Possible values V the units can take.
        If the level of measurement is not nominal, it must be ordered.

    distance_metric : callable
        Callable that return the distance of two given values.

    n_v : ndarray, with shape (V,)
        Number of pairable elements for each value.

    Returns
    -------
    d : ndarray, with shape (V, V)
        Distance matrix for each value pair.
    """
    return np.array([[distance_metric(v1, v2, i1=i1, i2=i2, n_v=n_v)
                      for i2, v2 in enumerate(value_domain)]
                     for i1, v1 in enumerate(value_domain)])