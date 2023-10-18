def _merge(options, name, bases, default=None):
    """Merges a named option collection."""
    result = None
    for base in bases:
        if base is None:
            continue

        value = getattr(base, name, None)
        if value is None:
            continue

        result = utils.cons(result, value)

    value = options.get(name)
    if value is not None:
        result = utils.cons(result, value)

    return result or default