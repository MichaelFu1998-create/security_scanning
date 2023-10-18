def timebinlc_worker(task):
    '''
    This is a parallel worker for the function below.

    Parameters
    ----------

    task : tuple
        This is of the form::

            task[0] = lcfile
            task[1] = binsizesec
            task[3] = {'outdir','lcformat','lcformatdir',
                       'timecols','magcols','errcols','minbinelems'}

    Returns
    -------

    str
        The output pickle file with the binned LC if successful. None otherwise.

    '''

    lcfile, binsizesec, kwargs = task

    try:
        binnedlc = timebinlc(lcfile, binsizesec, **kwargs)
        LOGINFO('%s binned using %s sec -> %s OK' %
                (lcfile, binsizesec, binnedlc))
        return binnedlc
    except Exception as e:
        LOGEXCEPTION('failed to bin %s using binsizesec = %s' % (lcfile,
                                                                 binsizesec))
        return None