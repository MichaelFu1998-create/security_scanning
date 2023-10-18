def _remote_call(f, *args, **kwargs):
    """(Executed on remote engine) convert Ids to real objects, call f """
    nargs = []
    for a in args:
        if isinstance(a, Id):
            nargs.append(distob.engine[a])
        elif (isinstance(a, collections.Sequence) and
                not isinstance(a, string_types)):
            nargs.append(
                    [distob.engine[b] if isinstance(b, Id) else b for b in a])
        else: nargs.append(a)
    for k, a in kwargs.items():
        if isinstance(a, Id):
            kwargs[k] = distob.engine[a]
        elif (isinstance(a, collections.Sequence) and
                not isinstance(a, string_types)):
            kwargs[k] = [
                    distob.engine[b] if isinstance(b, Id) else b for b in a]
    result = f(*nargs, **kwargs)
    if (isinstance(result, collections.Sequence) and
            not isinstance(result, string_types)):
        # We will return any sub-sequences by value, not recurse deeper
        results = []
        for subresult in result:
            if type(subresult) in distob.engine.proxy_types: 
                results.append(Ref(subresult))
            else:
                results.append(subresult)
        return results
    elif type(result) in distob.engine.proxy_types:
        return Ref(result)
    else:
        return result