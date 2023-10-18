def append_to_keys(adict, preffix):
    """
    Parameters
    ----------
    adict:
    preffix:

    Returns
    -------

    """
    return {preffix + str(key): (value if isinstance(value, dict) else value)
            for key, value in list(adict.items())}