def coerce(value1, value2, default=None):
    """Exclude NoSet objec

    .. code-block::

        >>> coerce(NoSet, 'value')
        'value'

    """
    if value1 is not NoSet:
        return value1
    elif value2 is not NoSet:
        return value2
    else:
        return default