def delete_taskrun(taskrun_id):
    """Delete the given taskrun.

    :param task: PYBOSSA task
    """
    try:
        res = _pybossa_req('delete', 'taskrun', taskrun_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise