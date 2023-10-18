def parallel_pf(lclist,
                outdir,
                timecols=None,
                magcols=None,
                errcols=None,
                lcformat='hat-sql',
                lcformatdir=None,
                pfmethods=('gls','pdm','mav','win'),
                pfkwargs=({},{},{},{}),
                sigclip=10.0,
                getblssnr=False,
                nperiodworkers=NCPUS,
                ncontrolworkers=1,
                liststartindex=None,
                listmaxobjects=None,
                minobservations=500,
                excludeprocessed=True):
    '''This drives the overall parallel period processing for a list of LCs.

    As a rough benchmark, 25000 HATNet light curves with up to 50000 points per
    LC take about 26 days in total for an invocation of this function using
    GLS+PDM+BLS, 10 periodworkers, and 4 controlworkers (so all 40 'cores') on a
    2 x Xeon E5-2660v3 machine.

    Parameters
    ----------

    lclist : list of str
        The list of light curve file to process.

    outdir : str
        The output directory where the period-finding result pickles will go.

    timecols : list of str or None
        The timecol keys to use from the lcdict in calculating the features.

    magcols : list of str or None
        The magcol keys to use from the lcdict in calculating the features.

    errcols : list of str or None
        The errcol keys to use from the lcdict in calculating the features.

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

    pfmethods : list of str
        This is a list of period finding methods to run. Each element is a
        string matching the keys of the `PFMETHODS` dict above. By default, this
        runs GLS, PDM, AoVMH, and the spectral window Lomb-Scargle periodogram.

    pfkwargs : list of dicts
        This is used to provide any special kwargs as dicts to each
        period-finding method function specified in `pfmethods`.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    getblssnr : bool
        If this is True and BLS is one of the methods specified in `pfmethods`,
        will also calculate the stats for each best period in the BLS results:
        transit depth, duration, ingress duration, refit period and epoch, and
        the SNR of the transit.

    nperiodworkers : int
        The number of parallel period-finding workers to launch per object task.

    ncontrolworkers : int
        The number of controlling processes to launch. This effectively sets how
        many objects from `lclist` will be processed in parallel.

    liststartindex : int or None
        This sets the index from where to start in `lclist`.

    listmaxobjects : int or None
        This sets the maximum number of objects in `lclist` to run
        period-finding for in this invocation. Together with `liststartindex`,
        `listmaxobjects` can be used to distribute processing over several
        independent machines if the number of light curves is very large.

    minobservations : int
        The minimum number of finite LC points required to process a light
        curve.

    excludeprocessed : bool
        If this is True, light curves that have existing period-finding result
        pickles in `outdir` will not be processed.

        FIXME: currently, this uses a dumb method of excluding already-processed
        files. A smarter way to do this is to (i) generate a SHA512 cachekey
        based on a repr of `{'lcfile', 'timecols', 'magcols', 'errcols',
        'lcformat', 'pfmethods', 'sigclip', 'getblssnr', 'pfkwargs'}`, (ii) make
        sure all list kwargs in the dict are sorted, (iii) check if the output
        file has the same cachekey in its filename (last 8 chars of cachekey
        should work), so the result was processed in exactly the same way as
        specifed in the input to this function, and can therefore be
        ignored. Will implement this later.

    Returns
    -------

    list of str
        A list of the period-finding pickles created for all of input LCs
        processed.

    '''

    # make the output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if (liststartindex is not None) and (listmaxobjects is None):
        lclist = lclist[liststartindex:]

    elif (liststartindex is None) and (listmaxobjects is not None):
        lclist = lclist[:listmaxobjects]

    elif (liststartindex is not None) and (listmaxobjects is not None):
        lclist = lclist[liststartindex:liststartindex+listmaxobjects]

    tasklist = [(x, outdir, timecols, magcols, errcols, lcformat, lcformatdir,
                 pfmethods, pfkwargs, getblssnr, sigclip, nperiodworkers,
                 minobservations,
                 excludeprocessed)
                for x in lclist]

    with ProcessPoolExecutor(max_workers=ncontrolworkers) as executor:
        resultfutures = executor.map(_runpf_worker, tasklist)

    results = [x for x in resultfutures]
    return results