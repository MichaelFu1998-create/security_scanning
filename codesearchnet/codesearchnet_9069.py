def _to_gen_(iterable):
    """
    Recursively iterate lists and tuples
    """
    from collections import Iterable

    for elm in iterable:
        if isinstance(elm, Iterable) and not isinstance(elm, (str, bytes)):
            yield from flatten(elm)
        else: yield elm