def _ars_to_proxies(ars):
    """wait for async results and return proxy objects
    Args: 
      ars: AsyncResult (or sequence of AsyncResults), each result type ``Ref``.
    Returns:
      Remote* proxy object (or list of them)
    """
    if (isinstance(ars, Remote) or
            isinstance(ars, numbers.Number) or
            ars is None):
        return ars
    elif isinstance(ars, collections.Sequence):
        res = []
        for i in range(len(ars)):
            res.append(_ars_to_proxies(ars[i]))
        return res
    elif isinstance(ars, ipyparallel.AsyncResult):
        ref = ars.r
        ObClass = ref.type
        if ObClass in distob.engine.proxy_types:
            RemoteClass = distob.engine.proxy_types[ObClass]
        else:
            RemoteClass = type(
                    'Remote' + ObClass.__name__, (Remote, ObClass), dict())
            RemoteClass = proxy_methods(ObClass)(RemoteClass)
        proxy_obj = RemoteClass(ref)
        return proxy_obj
    else:
        raise DistobTypeError('Unpacking ars: unexpected type %s' % type(ars))