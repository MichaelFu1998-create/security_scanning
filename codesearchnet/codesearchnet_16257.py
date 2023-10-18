def _flatten(iterable):
    """
    Given an iterable with nested iterables, generate a flat iterable
    """
    for i in iterable:
        if isinstance(i, Iterable) and not isinstance(i, string_types):
            for sub_i in _flatten(i):
                yield sub_i
        else:
            yield i