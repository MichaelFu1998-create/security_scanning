def filter_list(lst, filt):
    """
    Parameters
    ----------
    lst: list

    filter: function
        Unary string filter function

    Returns
    -------
    list
        List of items that passed the filter

    Example
    -------
    >>> l    = ['12123123', 'N123213']
    >>> filt = re.compile('\d*').match
    >>> nu_l = list_filter(l, filt)
    """
    return [m for s in lst for m in (filt(s),) if m]