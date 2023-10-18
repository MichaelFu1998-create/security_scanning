def contains(x):
    """Return true if this string or integer tuple appears in tables"""
    if isinstance(x, str):
        x = canonical_name(x)
        return x in _TO_COLOR_USER or x in _TO_COLOR
    else:
        x = tuple(x)
        return x in _TO_NAME_USER or x in _TO_NAME