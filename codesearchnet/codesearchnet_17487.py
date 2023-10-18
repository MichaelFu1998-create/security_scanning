def get_projects(limit=100, offset=0, last_id=None):
    """Return a list of registered projects.

    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last project, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of PYBOSSA Projects

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        print(OFFSET_WARNING)
        params = dict(limit=limit, offset=offset)
    try:
        res = _pybossa_req('get', 'project',
                           params=params)
        if type(res).__name__ == 'list':
            return [Project(project) for project in res]
        else:
            raise TypeError
    except:  # pragma: no cover
        raise