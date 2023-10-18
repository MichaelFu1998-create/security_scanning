def toposort_flatten(data, sort=True):
    """Returns a single list of dependencies. For any set returned by
toposort(), those items are sorted and appended to the result (just to
make the results deterministic)."""

    result = []
    for d in toposort(data):
        try:
            result.extend((sorted if sort else list)(d))
        except TypeError as e:
            result.extend(list(d))
    return result