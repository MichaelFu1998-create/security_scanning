def freeze(value):
    """ Cast value to its frozen counterpart. """
    if isinstance(value, list):
        return FrozenList(*value)
    if isinstance(value, dict):
        return FrozenDict(**value)
    return value