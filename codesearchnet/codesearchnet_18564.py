def to_str(prev, encoding=None):
    """Convert data from previous pipe with specified encoding."""
    first = next(prev)
    if isinstance(first, str):
        if encoding is None:
            yield first
            for s in prev:
                yield s
        else:
            yield first.encode(encoding)
            for s in prev:
                yield s.encode(encoding)
    else:
        if encoding is None:
            encoding = sys.stdout.encoding or 'utf-8'
        yield first.decode(encoding)
        for s in prev:
            yield s.decode(encoding)