def get_results(project_id, limit=100, offset=0, last_id=None):
    """Return a list of results for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :param last_id: id of the last result, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :type offset: integer
    :returns: True -- the response status code

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'result',
                           params=params)
        if type(res).__name__ == 'list':
            return [Result(result) for result in res]
        else:
            return res
    except:  # pragma: no cover
        raise