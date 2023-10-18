def iterable(obj, strok=False):
    """
    Checks if the input implements the iterator interface. An exception is made
    for strings, which return False unless `strok` is True

    Args:
        obj (object): a scalar or iterable input

        strok (bool): if True allow strings to be interpreted as iterable

    Returns:
        bool: True if the input is iterable

    Example:
        >>> obj_list = [3, [3], '3', (3,), [3, 4, 5], {}]
        >>> result = [iterable(obj) for obj in obj_list]
        >>> assert result == [False, True, False, True, True, True]
        >>> result = [iterable(obj, strok=True) for obj in obj_list]
        >>> assert result == [False, True, True, True, True, True]
    """
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return strok or not isinstance(obj, six.string_types)