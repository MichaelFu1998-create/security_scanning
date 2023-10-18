def parallel_update_objectinfo_cpdir(cpdir,
                                     cpglob='checkplot-*.pkl*',
                                     liststartindex=None,
                                     maxobjects=None,
                                     nworkers=NCPUS,
                                     fast_mode=False,
                                     findercmap='gray_r',
                                     finderconvolve=None,
                                     deredden_object=True,
                                     custom_bandpasses=None,
                                     gaia_submit_timeout=10.0,
                                     gaia_submit_tries=3,
                                     gaia_max_timeout=180.0,
                                     gaia_mirror=None,
                                     complete_query_later=True,
                                     lclistpkl=None,
                                     nbrradiusarcsec=60.0,
                                     maxnumneighbors=5,
                                     plotdpi=100,
                                     findercachedir='~/.astrobase/stamp-cache',
                                     verbose=True):
    '''This updates the objectinfo for a directory of checkplot pickles.

    Useful in cases where a previous round of GAIA/finderchart/external catalog
    acquisition failed. This will preserve the following keys in the checkplots
    if they exist:

    comments
    varinfo
    objectinfo.objecttags

    Parameters
    ----------

    cpdir : str
        The directory to look for checkplot pickles in.

    cpglob : str
        The UNIX fileglob to use when searching for checkplot pickle files.

    liststartindex : int
        The index of the input list to start working at.

    maxobjects : int
        The maximum number of objects to process in this run. Use this with
        `liststartindex` to effectively distribute working on a large list of
        input checkplot pickles over several sessions or machines.

    nworkers : int
        The number of parallel workers that will work on the checkplot
        update process.

    fast_mode : bool or float
        This runs the external catalog operations in a "fast" mode, with short
        timeouts and not trying to hit external catalogs that take a long time
        to respond. See the docstring for
        `checkplot.pkl_utils._pkl_finder_objectinfo` for details on how this
        works. If this is True, will run in "fast" mode with default timeouts (5
        seconds in most cases). If this is a float, will run in "fast" mode with
        the provided timeout value in seconds.

    findercmap : str or matplotlib.cm.Colormap object

    findercmap : str or matplotlib.cm.ColorMap object
        The Colormap object to use for the finder chart image.

    finderconvolve : astropy.convolution.Kernel object or None
        If not None, the Kernel object to use for convolving the finder image.

    deredden_objects : bool
        If this is True, will use the 2MASS DUST service to get extinction
        coefficients in various bands, and then try to deredden the magnitudes
        and colors of the object already present in the checkplot's objectinfo
        dict.

    custom_bandpasses : dict
        This is a dict used to provide custom bandpass definitions for any
        magnitude measurements in the objectinfo dict that are not automatically
        recognized by the `varclass.starfeatures.color_features` function. See
        its docstring for details on the required format.

    gaia_submit_timeout : float
        Sets the timeout in seconds to use when submitting a request to look up
        the object's information to the GAIA service. Note that if `fast_mode`
        is set, this is ignored.

    gaia_submit_tries : int
        Sets the maximum number of times the GAIA services will be contacted to
        obtain this object's information. If `fast_mode` is set, this is
        ignored, and the services will be contacted only once (meaning that a
        failure to respond will be silently ignored and no GAIA data will be
        added to the checkplot's objectinfo dict).

    gaia_max_timeout : float
        Sets the timeout in seconds to use when waiting for the GAIA service to
        respond to our request for the object's information. Note that if
        `fast_mode` is set, this is ignored.

    gaia_mirror : str
        This sets the GAIA mirror to use. This is a key in the
        `services.gaia.GAIA_URLS` dict which defines the URLs to hit for each
        mirror.

    complete_query_later : bool
        If this is True, saves the state of GAIA queries that are not yet
        complete when `gaia_max_timeout` is reached while waiting for the GAIA
        service to respond to our request. A later call for GAIA info on the
        same object will attempt to pick up the results from the existing query
        if it's completed. If `fast_mode` is True, this is ignored.

    lclistpkl : dict or str
        If this is provided, must be a dict resulting from reading a catalog
        produced by the `lcproc.catalogs.make_lclist` function or a str path
        pointing to the pickle file produced by that function. This catalog is
        used to find neighbors of the current object in the current light curve
        collection. Looking at neighbors of the object within the radius
        specified by `nbrradiusarcsec` is useful for light curves produced by
        instruments that have a large pixel scale, so are susceptible to
        blending of variability and potential confusion of neighbor variability
        with that of the actual object being looked at. If this is None, no
        neighbor lookups will be performed.

    nbrradiusarcsec : float
        The radius in arcseconds to use for a search conducted around the
        coordinates of this object to look for any potential confusion and
        blending of variability amplitude caused by their proximity.

    maxnumneighbors : int
        The maximum number of neighbors that will have their light curves and
        magnitudes noted in this checkplot as potential blends with the target
        object.

    plotdpi : int
        The resolution in DPI of the plots to generate in this function
        (e.g. the finder chart, etc.)

    findercachedir : str
        The path to the astrobase cache directory for finder chart downloads
        from the NASA SkyView service.

    verbose : bool
        If True, will indicate progress and warn about potential problems.

    Returns
    -------

    list of str
        Paths to the updated checkplot pickle file.

    '''

    cplist = sorted(glob.glob(os.path.join(cpdir, cpglob)))

    return parallel_update_objectinfo_cplist(
        cplist,
        liststartindex=liststartindex,
        maxobjects=maxobjects,
        nworkers=nworkers,
        fast_mode=fast_mode,
        findercmap=findercmap,
        finderconvolve=finderconvolve,
        deredden_object=deredden_object,
        custom_bandpasses=custom_bandpasses,
        gaia_submit_timeout=gaia_submit_timeout,
        gaia_submit_tries=gaia_submit_tries,
        gaia_max_timeout=gaia_max_timeout,
        gaia_mirror=gaia_mirror,
        complete_query_later=complete_query_later,
        lclistpkl=lclistpkl,
        nbrradiusarcsec=nbrradiusarcsec,
        maxnumneighbors=maxnumneighbors,
        plotdpi=plotdpi,
        findercachedir=findercachedir,
        verbose=verbose
    )