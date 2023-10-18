def flatten(nested_iterable):
    """
    Flattens arbitrarily nested lists/tuples.

    Code partially taken from https://stackoverflow.com/a/10824420.

    Parameters
    ----------
    nested_iterable
        A list or tuple of arbitrarily nested values.

    Yields
    ------
    any
        Non-list and non-tuple values in `nested_iterable`.

    """
    # don't just check if something is iterable here, because then strings
    # and arrays will be split into their characters and components
    if not isinstance(nested_iterable, (list, tuple)):
        yield nested_iterable
    else:
        for i in nested_iterable:
            if isinstance(i, (list, tuple)):
                for j in flatten(i):
                    yield j
            else:
                yield i