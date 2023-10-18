def gettrans(t):
    """
    Return a trans object

    Parameters
    ----------
    t : str | callable | type | trans
        name of transformation function

    Returns
    -------
    out : trans
    """
    obj = t
    # Make sure trans object is instantiated
    if isinstance(obj, str):
        name = '{}_trans'.format(obj)
        obj = globals()[name]()
    if callable(obj):
        obj = obj()
    if isinstance(obj, type):
        obj = obj()

    if not isinstance(obj, trans):
        raise ValueError("Could not get transform object.")

    return obj