def convert_result(r):
    """Waits for and converts any AsyncResults. Converts any Ref into a Remote.
    Args:
      r: can be an ordinary object, ipyparallel.AsyncResult, a Ref, or a
        Sequence of objects, AsyncResults and Refs.
    Returns: 
      either an ordinary object or a Remote instance"""
    if (isinstance(r, collections.Sequence) and
            not isinstance(r, string_types)):
        rs = []
        for subresult in r:
            rs.append(convert_result(subresult))
        return rs
    if isinstance(r, ipyparallel.AsyncResult):
        r = r.r
    if isinstance(r, Ref):
        RemoteClass = distob.engine.proxy_types[r.type]
        r = RemoteClass(r)
    return r