def get_taskruns(project_id, limit=100, offset=0, last_id=None):
    """Return a list of task runs for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last taskrun, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of task runs for the given project ID

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'taskrun',
                           params=params)
        if type(res).__name__ == 'list':
            return [TaskRun(taskrun) for taskrun in res]
        else:
            raise TypeError
    except:
        raise