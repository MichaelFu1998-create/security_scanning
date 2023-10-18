def periodrec_worker(task):
    '''This is a parallel worker for running period-recovery.

    Parameters
    ----------

    task : tuple
        This is used to pass args to the `periodicvar_recovery` function::

            task[0] = period-finding result pickle to work on
            task[1] = simbasedir
            task[2] = period_tolerance

    Returns
    -------

    dict
        This is the dict produced by the `periodicvar_recovery` function for the
        input period-finding result pickle.

    '''

    pfpkl, simbasedir, period_tolerance = task

    try:
        return periodicvar_recovery(pfpkl,
                                    simbasedir,
                                    period_tolerance=period_tolerance)

    except Exception as e:
        LOGEXCEPTION('periodic var recovery failed for %s' % repr(task))
        return None