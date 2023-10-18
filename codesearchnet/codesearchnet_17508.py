def find_results(project_id, **kwargs):
    """Return a list of matched results for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA Results members
    :type info: dict
    :rtype: list
    :returns: A list of results that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'result', params=kwargs)
        if type(res).__name__ == 'list':
            return [Result(result) for result in res]
        else:
            return res
    except:  # pragma: no cover
        raise