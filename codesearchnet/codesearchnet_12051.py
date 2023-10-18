def collection_worker(task):
    '''
    This wraps `process_fakelc` for `make_fakelc_collection` below.

    Parameters
    ----------

    task : tuple
        This is of the form::

            task[0] = lcfile
            task[1] = outdir
            task[2] = magrms
            task[3] = dict with keys: {'lcformat', 'timecols', 'magcols',
                                       'errcols', 'randomizeinfo'}

    Returns
    -------

    tuple
        This returns a tuple of the form::

            (fakelc_fpath,
             fakelc_lcdict['columns'],
             fakelc_lcdict['objectinfo'],
             fakelc_lcdict['moments'])
    '''

    lcfile, outdir, kwargs = task

    try:

        fakelcresults = make_fakelc(
            lcfile,
            outdir,
            **kwargs
        )

        return fakelcresults

    except Exception as e:

        LOGEXCEPTION('could not process %s into a fakelc' % lcfile)
        return None