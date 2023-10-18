def _async_scatter(obj, destination=None):
    """Distribute an obj or list to remote engines. 
    Return an async result or (possibly nested) lists of async results, 
    each of which is a Ref
    """
    #TODO Instead of special cases for strings and Remote, should have a
    #     list of types that should not be proxied, inc. strings and Remote.
    if (isinstance(obj, Remote) or 
            isinstance(obj, numbers.Number) or 
            obj is None):
        return obj
    if (isinstance(obj, collections.Sequence) and 
            not isinstance(obj, string_types)):
        ars = []
        if destination is not None:
            assert(len(destination) == len(obj))
            for i in range(len(obj)):
                ars.append(_async_scatter(obj[i], destination[i]))
        else:
            for i in range(len(obj)):
                ars.append(_async_scatter(obj[i], destination=None))
        return ars
    else:
        if distob.engine is None:
            setup_engines()
        client = distob.engine._client
        dv = distob.engine._dv
        def remote_put(obj):
            return Ref(obj)
        if destination is not None:
            assert(isinstance(destination, numbers.Integral))
            dv.targets = destination
        else:
            dv.targets = _async_scatter.next_engine
            _async_scatter.next_engine = (
                    _async_scatter.next_engine + 1) % len(client)
        ar_ref = dv.apply_async(remote_put, obj)
        dv.targets = client.ids
        return ar_ref