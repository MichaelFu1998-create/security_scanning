def _parallel_tfa_worker(task):
    '''
    This is a parallel worker for the function below.

    task[0] = lcfile
    task[1] = timecol
    task[2] = magcol
    task[3] = errcol
    task[4] = templateinfo
    task[5] = lcformat
    task[6] = lcformatdir
    task[6] = interp
    task[7] = sigclip

    '''

    (lcfile, timecol, magcol, errcol,
     templateinfo, lcformat, lcformatdir,
     interp, sigclip, mintemplatedist_arcmin) = task

    try:

        res = apply_tfa_magseries(
            lcfile, timecol, magcol, errcol,
            templateinfo,
            lcformat=lcformat,
            lcformatdir=lcformatdir,
            interp=interp,
            sigclip=sigclip,
            mintemplatedist_arcmin=mintemplatedist_arcmin
        )
        if res:
            LOGINFO('%s -> %s TFA OK' % (lcfile, res))
        return res

    except Exception as e:

        LOGEXCEPTION('TFA failed for %s' % lcfile)
        return None