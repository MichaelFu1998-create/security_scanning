def find_category(**kwargs):
    """Return a list with matching Category arguments.

    :param kwargs: PYBOSSA Category members
    :rtype: list
    :returns: A list of project that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'category', params=kwargs)
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            return res
    except:  # pragma: no cover
        raise