def get_categories(limit=20, offset=0, last_id=None):
    """Return a list of registered categories.

    :param limit: Number of returned items, default 20
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last category, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of PYBOSSA Categories

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
    try:
        res = _pybossa_req('get', 'category',
                           params=params)
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            raise TypeError
    except:
        raise