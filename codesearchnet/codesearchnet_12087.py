def cp_objectinfo_worker(task):
    '''This is a parallel worker for `parallel_update_cp_objectinfo`.

    Parameters
    ----------

    task : tuple
        - task[0] = checkplot pickle file
        - task[1] = kwargs

    Returns
    -------

    str
        The name of the checkplot file that was updated. None if the update
        fails for some reason.

    '''

    cpf, cpkwargs = task

    try:

        newcpf = update_checkplot_objectinfo(cpf, **cpkwargs)
        return newcpf

    except Exception as e:
        LOGEXCEPTION('failed to update objectinfo for %s' % cpf)
        return None