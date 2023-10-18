def create_task(project_id, info, n_answers=30, priority_0=0, quorum=0):
    """Create a task for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param info: PYBOSSA Project info JSON field
    :type info: dict
    :param n_answers: Number of answers or TaskRuns per task, default 30
    :type n_answers: integer
    :param priority_0: Value between 0 and 1 indicating priority of task within
        Project (higher = more important), default 0.0
    :type priority_0: float
    :param quorum: Number of times this task should be done by different users,
        default 0
    :type quorum: integer
    :returns: True -- the response status code
    """
    try:
        task = dict(
            project_id=project_id,
            info=info,
            calibration=0,
            priority_0=priority_0,
            n_answers=n_answers,
            quorum=quorum
        )
        res = _pybossa_req('post', 'task', payload=task)
        if res.get('id'):
            return Task(res)
        else:
            return res
    except:  # pragma: no cover
        raise