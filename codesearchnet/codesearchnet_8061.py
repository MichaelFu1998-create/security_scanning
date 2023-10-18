def serialize(transform, **kwargs):
    '''Serialize a transformation object or pipeline.

    Parameters
    ----------
    transform : BaseTransform or Pipeline
        The transformation object to be serialized

    kwargs
        Additional keyword arguments to `jsonpickle.encode()`

    Returns
    -------
    json_str : str
        A JSON encoding of the transformation

    See Also
    --------
    deserialize

    Examples
    --------
    >>> D = muda.deformers.TimeStretch(rate=1.5)
    >>> muda.serialize(D)
    '{"params": {"rate": 1.5},
      "__class__": {"py/type": "muda.deformers.time.TimeStretch"}}'
    '''

    params = transform.get_params()
    return jsonpickle.encode(params, **kwargs)