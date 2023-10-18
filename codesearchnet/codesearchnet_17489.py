def find_project(**kwargs):
    """Return a list with matching project arguments.

    :param kwargs: PYBOSSA Project members
    :rtype: list
    :returns: A list of projects that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'project', params=kwargs)
        if type(res).__name__ == 'list':
            return [Project(project) for project in res]
        else:
            return res
    except:  # pragma: no cover
        raise