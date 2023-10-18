def dmap(fn, record):
    """map for a directory"""
    values = (fn(v) for k, v in record.items())
    return dict(itertools.izip(record, values))