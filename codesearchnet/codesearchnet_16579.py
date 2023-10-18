def _coincidences(value_counts, value_domain, dtype=np.float64):
    """Coincidence matrix.

    Parameters
    ----------
    value_counts : ndarray, with shape (N, V)
        Number of coders that assigned a certain value to a determined unit, where N is the number of units
        and V is the value count.

    value_domain : array_like, with shape (V,)
        Possible values V the units can take.
        If the level of measurement is not nominal, it must be ordered.

    dtype : data-type
        Result and computation data-type.

    Returns
    -------
    o : ndarray, with shape (V, V)
        Coincidence matrix.
    """
    value_counts_matrices = value_counts.reshape(value_counts.shape + (1,))
    pairable = np.maximum(np.sum(value_counts, axis=1), 2)
    diagonals = np.tile(np.eye(len(value_domain)), (len(value_counts), 1, 1)) \
        * value_counts.reshape((value_counts.shape[0], 1, value_counts.shape[1]))
    unnormalized_coincidences = value_counts_matrices * value_counts_matrices.transpose((0, 2, 1)) - diagonals
    return np.sum(np.divide(unnormalized_coincidences, (pairable - 1).reshape((-1, 1, 1)), dtype=dtype), axis=0)