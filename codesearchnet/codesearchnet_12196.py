def runcp_worker(task):
    '''
    This is the worker for running checkplots.

    Parameters
    ----------

    task : tuple
        This is of the form: (pfpickle, outdir, lcbasedir, kwargs).

    Returns
    -------

    list of str
        The list of checkplot pickles returned by the `runcp` function.

    '''

    pfpickle, outdir, lcbasedir, kwargs = task

    try:

        return runcp(pfpickle, outdir, lcbasedir, **kwargs)

    except Exception as e:

        LOGEXCEPTION(' could not make checkplots for %s: %s' % (pfpickle, e))
        return None