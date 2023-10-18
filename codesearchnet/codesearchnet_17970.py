def aN(a, dim=3, dtype='int'):
    """
    Convert an integer or iterable list to numpy array of length dim. This func
    is used to allow other methods to take both scalars non-numpy arrays with
    flexibility.

    Parameters
    ----------
    a : number, iterable, array-like
        The object to convert to numpy array

    dim : integer
        The length of the resulting array

    dtype : string or np.dtype
        Type which the resulting array should be, e.g. 'float', np.int8

    Returns
    -------
    arr : numpy array
        Resulting numpy array of length ``dim`` and type ``dtype``

    Examples
    --------
    >>> aN(1, dim=2, dtype='float')
    array([ 1.,  1.])

    >>> aN(1, dtype='int')
    array([1, 1, 1])

    >>> aN(np.array([1,2,3]), dtype='float')
    array([ 1.,  2.,  3.])
    """
    if not hasattr(a, '__iter__'):
        return np.array([a]*dim, dtype=dtype)
    return np.array(a).astype(dtype)