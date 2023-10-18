def _random_coincidences(value_domain, n, n_v):
    """Random coincidence matrix.

    Parameters
    ----------
    value_domain : array_like, with shape (V,)
        Possible values V the units can take.
        If the level of measurement is not nominal, it must be ordered.

    n : scalar
        Number of pairable values.

    n_v : ndarray, with shape (V,)
        Number of pairable elements for each value.

    Returns
    -------
    e : ndarray, with shape (V, V)
        Random coincidence matrix.
    """
    n_v_column = n_v.reshape(-1, 1)
    return (n_v_column.dot(n_v_column.T) - np.eye(len(value_domain)) * n_v_column) / (n - 1)