def all_named_colors():
    """Return an iteration over all name, color pairs in tables"""
    yield from _TO_COLOR_USER.items()
    for name, color in _TO_COLOR.items():
        if name not in _TO_COLOR_USER:
            yield name, color