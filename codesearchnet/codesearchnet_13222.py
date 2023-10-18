def summary(obj, indent=0):
    '''Helper function to format repr strings for JObjects and friends.

    Parameters
    ----------
    obj
        The object to repr

    indent : int >= 0
        indent each new line by `indent` spaces

    Returns
    -------
    r : str
        If `obj` has a `__summary__` method, it is used.

        If `obj` is a `SortedKeyList`, then it returns a description
        of the length of the list.

        Otherwise, `repr(obj)`.
    '''
    if hasattr(obj, '__summary__'):
        rep = obj.__summary__()
    elif isinstance(obj, SortedKeyList):
        rep = '<{:d} observations>'.format(len(obj))
    else:
        rep = repr(obj)

    return rep.replace('\n', '\n' + ' ' * indent)