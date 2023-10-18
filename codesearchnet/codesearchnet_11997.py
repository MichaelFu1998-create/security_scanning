def parallel_epd_worker(task):
    '''This is a parallel worker for the function below.

    Parameters
    ----------

    task : tuple
        - task[0] = lcfile
        - task[1] = timecol
        - task[2] = magcol
        - task[3] = errcol
        - task[4] = externalparams
        - task[5] = lcformat
        - task[6] = lcformatdir
        - task[7] = epdsmooth_sigclip
        - task[8] = epdsmooth_windowsize
        - task[9] = epdsmooth_func
        - task[10] = epdsmooth_extraparams

    Returns
    -------

    str or None
        If EPD succeeds for an input LC, returns the filename of the output EPD
        LC pickle file. If it fails, returns None.

    '''

    (lcfile, timecol, magcol, errcol,
     externalparams, lcformat, lcformatdir, magsarefluxes,
     epdsmooth_sigclip, epdsmooth_windowsize,
     epdsmooth_func, epdsmooth_extraparams) = task

    try:

        epd = apply_epd_magseries(lcfile,
                                  timecol,
                                  magcol,
                                  errcol,
                                  externalparams,
                                  lcformat=lcformat,
                                  lcformatdir=lcformatdir,
                                  epdsmooth_sigclip=epdsmooth_sigclip,
                                  epdsmooth_windowsize=epdsmooth_windowsize,
                                  epdsmooth_func=epdsmooth_func,
                                  epdsmooth_extraparams=epdsmooth_extraparams)
        if epd is not None:
            LOGINFO('%s -> %s EPD OK' % (lcfile, epd))
            return epd
        else:
            LOGERROR('EPD failed for %s' % lcfile)
            return None

    except Exception as e:

        LOGEXCEPTION('EPD failed for %s' % lcfile)
        return None