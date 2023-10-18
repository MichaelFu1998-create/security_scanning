def filter_dict(unfiltered, filter_keys):
    """Return a subset of a dictionary using the specified keys."""
    filtered = DotDict()
    for k in filter_keys:
        filtered[k] = unfiltered[k]
    return filtered