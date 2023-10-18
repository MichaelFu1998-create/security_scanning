def find_tasks(project_id, **kwargs):
    """Return a list of matched tasks for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA Task members
    :type info: dict
    :rtype: list
    :returns: A list of tasks that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'task', params=kwargs)
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:  # pragma: no cover
        raise