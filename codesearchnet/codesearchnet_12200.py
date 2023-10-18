def _runpf_worker(task):
    '''
    This runs the runpf function.

    '''

    (lcfile, outdir, timecols, magcols, errcols, lcformat, lcformatdir,
     pfmethods, pfkwargs, getblssnr, sigclip, nworkers, minobservations,
     excludeprocessed) = task

    if os.path.exists(lcfile):
        pfresult = runpf(lcfile,
                         outdir,
                         timecols=timecols,
                         magcols=magcols,
                         errcols=errcols,
                         lcformat=lcformat,
                         lcformatdir=lcformatdir,
                         pfmethods=pfmethods,
                         pfkwargs=pfkwargs,
                         getblssnr=getblssnr,
                         sigclip=sigclip,
                         nworkers=nworkers,
                         minobservations=minobservations,
                         excludeprocessed=excludeprocessed)
        return pfresult
    else:
        LOGERROR('LC does not exist for requested file %s' % lcfile)
        return None