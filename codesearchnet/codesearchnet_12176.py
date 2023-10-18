def _varfeatures_worker(task):
    '''
    This wraps varfeatures.

    '''

    try:
        (lcfile, outdir, timecols, magcols, errcols,
         mindet, lcformat, lcformatdir) = task
        return get_varfeatures(lcfile, outdir,
                               timecols=timecols,
                               magcols=magcols,
                               errcols=errcols,
                               mindet=mindet,
                               lcformat=lcformat,
                               lcformatdir=lcformatdir)

    except Exception as e:
        return None