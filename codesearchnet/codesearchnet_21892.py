def call(f, *args, **kwargs):
    """Execute f on the arguments, either locally or remotely as appropriate.
    If there are multiple remote arguments, they must be on the same engine.
    
    kwargs:
      prefer_local (bool, optional): Whether to return cached local results if
        available, in preference to returning Remote objects. Default is True.
      block (bool, optional): Whether remote calls should be synchronous.
        If False, returned results may be AsyncResults and should be converted
        by the caller using convert_result() before use. Default is True.
    """
    this_engine = distob.engine.eid
    prefer_local = kwargs.pop('prefer_local', True)
    block = kwargs.pop('block', True)
    execloc, args, kwargs = _process_args(args, kwargs, prefer_local)
    if execloc is this_engine:
        r = f(*args, **kwargs)
    else:
        if False and prefer_local:
            # result cache disabled until issue mattja/distob#1 is fixed
            try:
                kwtuple = tuple((k, kwargs[k]) for k in sorted(kwargs.keys()))
                key = (f, args, kwtuple)
                r = _call_cache[key]
            except TypeError as te:
                if te.args[0][:10] == 'unhashable':
                    #print("unhashable. won't be able to cache")
                    r = _uncached_call(execloc, f, *args, **kwargs)
                else:
                    raise
            except KeyError:
                r = _uncached_call(execloc, f, *args, **kwargs)
                if block:
                    _call_cache[key] = r.r
        else:
            r = _uncached_call(execloc, f, *args, **kwargs)
    if block:
        return convert_result(r)
    else:
        return r