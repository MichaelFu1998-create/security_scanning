def filter_objlist(olist, fieldname, fieldval):
    """
    Returns a list with of the objects in olist that have a fieldname valued as fieldval

    Parameters
    ----------
    olist: list of objects

    fieldname: string

    fieldval: anything

    Returns
    -------
    list of objets
    """
    return [x for x in olist if getattr(x, fieldname) == fieldval]