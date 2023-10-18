def _encode_ids(*args):
    """
    Do url-encode resource ids
    """

    ids = []
    for v in args:
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            ids.append(urllib.quote(qv))
        else:
            qv = str(v)
            ids.append(urllib.quote(qv))

    return ';'.join(ids)