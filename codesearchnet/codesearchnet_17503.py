def delete_task(task_id):
    """Delete a task for a given task ID.

    :param task: PYBOSSA task

    """
    #: :arg task: A task
    try:
        res = _pybossa_req('delete', 'task', task_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise