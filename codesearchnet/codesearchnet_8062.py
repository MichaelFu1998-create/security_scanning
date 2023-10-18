def deserialize(encoded, **kwargs):
    '''Construct a muda transformation from a JSON encoded string.

    Parameters
    ----------
    encoded : str
        JSON encoding of the transformation or pipeline

    kwargs
        Additional keyword arguments to `jsonpickle.decode()`

    Returns
    -------
    obj
        The transformation

    See Also
    --------
    serialize

    Examples
    --------
    >>> D = muda.deformers.TimeStretch(rate=1.5)
    >>> D_serial = muda.serialize(D)
    >>> D2 = muda.deserialize(D_serial)
    >>> D2
    TimeStretch(rate=1.5)
    '''

    params = jsonpickle.decode(encoded, **kwargs)

    return __reconstruct(params)