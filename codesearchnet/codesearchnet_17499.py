def get_tasks(project_id, limit=100, offset=0, last_id=None):
    """Return a list of tasks for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :param last_id: id of the last task, used for pagination. If provided, offset is ignored
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
        res = _pybossa_req('get', 'task',
                           params=params)
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:  # pragma: no cover
        raise