def parallel_timebin_lcdir(lcdir,
                           binsizesec,
                           maxobjects=None,
                           outdir=None,
                           lcformat='hat-sql',
                           lcformatdir=None,
                           timecols=None,
                           magcols=None,
                           errcols=None,
                           minbinelems=7,
                           nworkers=NCPUS,
                           maxworkertasks=1000):
    '''
    This time bins all the light curves in the specified directory.

    Parameters
    ----------

    lcdir : list of str
        Directory containing the input LCs to process.

    binsizesec : float
        The time bin size to use in seconds.

    maxobjects : int or None
        If provided, LC processing will stop at `lclist[maxobjects]`.

    outdir : str or None
        The directory where output LCs will be written. If None, will write to
        the same directory as the input LCs.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curve file.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    timecols,magcols,errcols : lists of str
        The keys in the lcdict produced by your light curve reader function that
        correspond to the times, mags/fluxes, and associated measurement errors
        that will be used as inputs to the binning process. If these are None,
        the default values for `timecols`, `magcols`, and `errcols` for your
        light curve format will be used here.

    minbinelems : int
        The minimum number of time-bin elements required to accept a time-bin as
        valid for the output binned light curve.

    nworkers : int
        Number of parallel workers to launch.

    maxworkertasks : int
        The maximum number of tasks a parallel worker will complete before being
        replaced to guard against memory leaks.

    Returns
    -------

    dict
        The returned dict contains keys = input LCs, vals = output LCs.

    '''
    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (fileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    lclist = sorted(glob.glob(os.path.join(lcdir, fileglob)))

    return parallel_timebin(lclist,
                            binsizesec,
                            maxobjects=maxobjects,
                            outdir=outdir,
                            lcformat=lcformat,
                            timecols=timecols,
                            magcols=magcols,
                            errcols=errcols,
                            minbinelems=minbinelems,
                            nworkers=nworkers,
                            maxworkertasks=maxworkertasks)