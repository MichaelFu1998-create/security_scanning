def parallel_cp(
        pfpicklelist,
        outdir,
        lcbasedir,
        fast_mode=False,
        lcfnamelist=None,
        cprenorm=False,
        lclistpkl=None,
        gaia_max_timeout=60.0,
        gaia_mirror=None,
        nbrradiusarcsec=60.0,
        maxnumneighbors=5,
        makeneighborlcs=True,
        xmatchinfo=None,
        xmatchradiusarcsec=3.0,
        sigclip=10.0,
        minobservations=99,
        lcformat='hat-sql',
        lcformatdir=None,
        timecols=None,
        magcols=None,
        errcols=None,
        skipdone=False,
        done_callback=None,
        done_callback_args=None,
        done_callback_kwargs=None,
        liststartindex=None,
        maxobjects=None,
        nworkers=NCPUS,
):
    '''This drives the parallel execution of `runcp` for a list of periodfinding
    result pickles.

    Parameters
    ----------

    pfpicklelist : list of str or list of Nones
        This is the list of the filenames of the period-finding result pickles
        to process. To make checkplots using the light curves directly, set this
        to a list of Nones with the same length as the list of light curve files
        that you provide in `lcfnamelist`.

    outdir : str
        The directory the checkplot pickles will be written to.

    lcbasedir : str
        The base directory that this function will look in to find the light
        curves pointed to by the period-finding result files. If you're using
        `lcfnamelist` to provide a list of light curve filenames directly, this
        arg is ignored.

    lcfnamelist : list of str or None
        If this is provided, it must be a list of the input light curve
        filenames to process. These can either be associated with each input
        period-finder result pickle, or can be provided standalone to make
        checkplots without phased LC plots in them. In the second case, you must
        set `pfpicklelist` to a list of Nones that matches the length of
        `lcfnamelist`.

    cprenorm : bool
        Set this to True if the light curves should be renormalized by
        `checkplot.checkplot_pickle`. This is set to False by default because we
        do our own normalization in this function using the light curve's
        registered normalization function and pass the normalized times, mags,
        errs to the `checkplot.checkplot_pickle` function.

    lclistpkl : str or dict
        This is either the filename of a pickle or the actual dict produced by
        lcproc.make_lclist. This is used to gather neighbor information.

    nbrradiusarcsec : float
        The radius in arcseconds to use for a search conducted around the
        coordinates of this object to look for any potential confusion and
        blending of variability amplitude caused by their proximity.

    maxnumneighbors : int
        The maximum number of neighbors that will have their light curves and
        magnitudes noted in this checkplot as potential blends with the target
        object.

    makeneighborlcs : bool
        If True, will make light curve and phased light curve plots for all
        neighbors found in the object collection for each input object.

    fast_mode : bool or float
        This runs the external catalog operations in a "fast" mode, with short
        timeouts and not trying to hit external catalogs that take a long time
        to respond.

        If this is set to True, the default settings for the external requests
        will then become::

                skyview_lookup = False
                skyview_timeout = 10.0
                skyview_retry_failed = False
                dust_timeout = 10.0
                gaia_submit_timeout = 7.0
                gaia_max_timeout = 10.0
                gaia_submit_tries = 2
                complete_query_later = False
                search_simbad = False

        If this is a float, will run in "fast" mode with the provided timeout
        value in seconds and the following settings::

                skyview_lookup = True
                skyview_timeout = fast_mode
                skyview_retry_failed = False
                dust_timeout = fast_mode
                gaia_submit_timeout = 0.66*fast_mode
                gaia_max_timeout = fast_mode
                gaia_submit_tries = 2
                complete_query_later = False
                search_simbad = False

    gaia_max_timeout : float
        Sets the timeout in seconds to use when waiting for the GAIA service to
        respond to our request for the object's information. Note that if
        `fast_mode` is set, this is ignored.

    gaia_mirror : str or None
        This sets the GAIA mirror to use. This is a key in the
        `services.gaia.GAIA_URLS` dict which defines the URLs to hit for each
        mirror.

    xmatchinfo : str or dict
        This is either the xmatch dict produced by the function
        `load_xmatch_external_catalogs` above, or the path to the xmatch info
        pickle file produced by that function.

    xmatchradiusarcsec : float
        This is the cross-matching radius to use in arcseconds.

    minobservations : int
        The minimum of observations the input object's mag/flux time-series must
        have for this function to plot its light curve and phased light
        curve. If the object has less than this number, no light curves will be
        plotted, but the checkplotdict will still contain all of the other
        information.

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

    timecols : list of str or None
        The timecol keys to use from the lcdict in generating this checkplot.

    magcols : list of str or None
        The magcol keys to use from the lcdict in generating this checkplot.

    errcols : list of str or None
        The errcol keys to use from the lcdict in generating this checkplot.

    skipdone : bool
        This indicates if this function will skip creating checkplots that
        already exist corresponding to the current `objectid` and `magcol`. If
        `skipdone` is set to True, this will be done.

    done_callback : Python function or None
        This is used to provide a function to execute after the checkplot
        pickles are generated. This is useful if you want to stream the results
        of checkplot making to some other process, e.g. directly running an
        ingestion into an LCC-Server collection. The function will always get
        the list of the generated checkplot pickles as its first arg, and all of
        the kwargs for runcp in the kwargs dict. Additional args and kwargs can
        be provided by giving a list in the `done_callbacks_args` kwarg and a
        dict in the `done_callbacks_kwargs` kwarg.

        NOTE: the function you pass in here should be pickleable by normal
        Python if you want to use it with the parallel_cp and parallel_cp_lcdir
        functions below.

    done_callback_args : tuple or None
        If not None, contains any args to pass into the `done_callback`
        function.

    done_callback_kwargs : dict or None
        If not None, contains any kwargs to pass into the `done_callback`
        function.

    liststartindex : int
        The index of the `pfpicklelist` (and `lcfnamelist` if provided) to start
        working at.

    maxobjects : int
        The maximum number of objects to process in this run. Use this with
        `liststartindex` to effectively distribute working on a large list of
        input period-finding result pickles (and light curves if `lcfnamelist`
        is also provided) over several sessions or machines.

    nworkers : int
        The number of parallel workers that will work on the checkplot
        generation process.

    Returns
    -------

    dict
        This returns a dict with keys = input period-finding pickles and vals =
        list of the corresponding checkplot pickles produced.

    '''

    # work around the Darwin segfault after fork if no network activity in
    # main thread bug: https://bugs.python.org/issue30385#msg293958
    if sys.platform == 'darwin':
        import requests
        requests.get('http://captive.apple.com/hotspot-detect.html')

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # handle the start and end indices
    if (liststartindex is not None) and (maxobjects is None):
        pfpicklelist = pfpicklelist[liststartindex:]
        if lcfnamelist is not None:
            lcfnamelist = lcfnamelist[liststartindex:]

    elif (liststartindex is None) and (maxobjects is not None):
        pfpicklelist = pfpicklelist[:maxobjects]
        if lcfnamelist is not None:
            lcfnamelist = lcfnamelist[:maxobjects]

    elif (liststartindex is not None) and (maxobjects is not None):
        pfpicklelist = (
            pfpicklelist[liststartindex:liststartindex+maxobjects]
        )
        if lcfnamelist is not None:
            lcfnamelist = lcfnamelist[liststartindex:liststartindex+maxobjects]

    # if the lcfnamelist is not provided, create a dummy
    if lcfnamelist is None:
        lcfnamelist = [None]*len(pfpicklelist)

    tasklist = [(x, outdir, lcbasedir,
                 {'lcformat':lcformat,
                  'lcformatdir':lcformatdir,
                  'lcfname':y,
                  'timecols':timecols,
                  'magcols':magcols,
                  'errcols':errcols,
                  'lclistpkl':lclistpkl,
                  'gaia_max_timeout':gaia_max_timeout,
                  'gaia_mirror':gaia_mirror,
                  'nbrradiusarcsec':nbrradiusarcsec,
                  'maxnumneighbors':maxnumneighbors,
                  'makeneighborlcs':makeneighborlcs,
                  'xmatchinfo':xmatchinfo,
                  'xmatchradiusarcsec':xmatchradiusarcsec,
                  'sigclip':sigclip,
                  'minobservations':minobservations,
                  'skipdone':skipdone,
                  'cprenorm':cprenorm,
                  'fast_mode':fast_mode,
                  'done_callback':done_callback,
                  'done_callback_args':done_callback_args,
                  'done_callback_kwargs':done_callback_kwargs}) for
                x,y in zip(pfpicklelist, lcfnamelist)]

    resultfutures = []
    results = []

    with ProcessPoolExecutor(max_workers=nworkers) as executor:
        resultfutures = executor.map(runcp_worker, tasklist)

    results = [x for x in resultfutures]

    executor.shutdown()
    return results