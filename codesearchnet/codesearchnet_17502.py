def update_task(task):
    """Update a task for a given task ID.

    :param task: PYBOSSA task

    """
    try:
        task_id = task.id
        task = _forbidden_attributes(task)
        res = _pybossa_req('put', 'task', task_id, payload=task.data)
        if res.get('id'):
            return Task(res)
        else:
            return res
    except:  # pragma: no cover
        raise