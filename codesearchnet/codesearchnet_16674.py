def tuplize_key(obj, key, remove_extra=False):
    """Args"""

    paramlen = len(obj.formula.parameters)

    if isinstance(key, str):
        key = (key,)
    elif not isinstance(key, Sequence):
        key = (key,)

    if not remove_extra:
        return key
    else:
        arglen = len(key)
        if arglen:
            return key[: min(arglen, paramlen)]
        else:
            return key