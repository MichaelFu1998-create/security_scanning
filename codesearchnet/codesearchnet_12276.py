def parallel_tfa_lcdir(lcdir,
                       templateinfo,
                       lcfileglob=None,
                       timecols=None,
                       magcols=None,
                       errcols=None,
                       lcformat='hat-sql',
                       lcformatdir=None,
                       interp='nearest',
                       sigclip=5.0,
                       mintemplatedist_arcmin=10.0,
                       nworkers=NCPUS,
                       maxworkertasks=1000):
    '''This applies TFA in parallel to all LCs in a directory.

    Parameters
    ----------

    lcdir : str
        This is the directory containing the light curve files to process..

    templateinfo : dict or str
        This is either the dict produced by `tfa_templates_lclist` or the pickle
        produced by the same function.

    lcfileglob : str or None
        The UNIX file glob to use when searching for light curve files in
        `lcdir`. If None, the default file glob associated with registered LC
        format provided is used.

    timecols : list of str or None
        The timecol keys to use from the lcdict in applying TFA corrections.

    magcols : list of str or None
        The magcol keys to use from the lcdict in applying TFA corrections.

    errcols : list of str or None
        The errcol keys to use from the lcdict in applying TFA corrections.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    interp : str
        This is passed to scipy.interpolate.interp1d as the kind of
        interpolation to use when reforming the light curves to the timebase of
        the TFA templates.

    sigclip : float or sequence of two floats or None
        This is the sigma clip to apply to the light curves before running TFA
        on it.

    mintemplatedist_arcmin : float
        This sets the minimum distance required from the target object for
        objects in the TFA template ensemble. Objects closer than this distance
        will be removed from the ensemble.

    nworkers : int
        The number of parallel workers to launch

    maxworkertasks : int
        The maximum number of tasks per worker allowed before it's replaced by a
        fresh one.

    Returns
    -------

    dict
        Contains the input file names and output TFA light curve filenames per
        input file organized by each `magcol` in `magcols`.

    '''

    # open the templateinfo first
    if isinstance(templateinfo,str) and os.path.exists(templateinfo):
        with open(templateinfo,'rb') as infd:
            templateinfo = pickle.load(infd)

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (dfileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    # find all the files matching the lcglob in lcdir
    if lcfileglob is None:
        lcfileglob = dfileglob

    lclist = sorted(glob.glob(os.path.join(lcdir, lcfileglob)))

    return parallel_tfa_lclist(
        lclist,
        templateinfo,
        timecols=timecols,
        magcols=magcols,
        errcols=errcols,
        lcformat=lcformat,
        lcformatdir=None,
        interp=interp,
        sigclip=sigclip,
        mintemplatedist_arcmin=mintemplatedist_arcmin,
        nworkers=nworkers,
        maxworkertasks=maxworkertasks
    )