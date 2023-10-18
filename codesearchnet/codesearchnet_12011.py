def checkplot_pickle(
        lspinfolist,
        times,
        mags,
        errs,
        fast_mode=False,
        magsarefluxes=False,
        nperiodstouse=3,
        objectinfo=None,
        deredden_object=True,
        custom_bandpasses=None,
        gaia_submit_timeout=10.0,
        gaia_submit_tries=3,
        gaia_max_timeout=180.0,
        gaia_mirror=None,
        complete_query_later=True,
        varinfo=None,
        getvarfeatures=True,
        lclistpkl=None,
        nbrradiusarcsec=60.0,
        maxnumneighbors=5,
        xmatchinfo=None,
        xmatchradiusarcsec=3.0,
        lcfitfunc=None,
        lcfitparams=None,
        externalplots=None,
        findercmap='gray_r',
        finderconvolve=None,
        findercachedir='~/.astrobase/stamp-cache',
        normto='globalmedian',
        normmingap=4.0,
        sigclip=4.0,
        varepoch='min',
        phasewrap=True,
        phasesort=True,
        phasebin=0.002,
        minbinelems=7,
        plotxlim=(-0.8,0.8),
        xliminsetmode=False,
        plotdpi=100,
        bestperiodhighlight=None,
        xgridlines=None,
        mindet=99,
        verbose=True,
        outfile=None,
        outgzip=False,
        pickleprotocol=None,
        returndict=False
):

    '''This writes a multiple lspinfo checkplot to a (gzipped) pickle file.

    This function can take input from multiple lspinfo dicts (e.g. a list of
    output dicts or gzipped pickles of dicts from independent runs of BLS, PDM,
    AoV, or GLS period-finders in periodbase).

    NOTE: if `lspinfolist` contains more than one lspinfo object with the same
    lspmethod ('pdm','gls','sls','aov','bls'), the latest one in the list will
    overwrite the earlier ones.

    The output dict contains all the plots (magseries and phased magseries),
    periodograms, object information, variability information, light curves, and
    phased light curves. This can be written to:

    - a pickle with `checkplot_pickle` below
    - a PNG with `checkplot.pkl_png.checkplot_pickle_to_png`

    Parameters
    ----------

    lspinfolist : list of dicts
        This is a list of dicts containing period-finder results ('lspinfo'
        dicts). These can be from any of the period-finder methods in
        astrobase.periodbase. To incorporate external period-finder results into
        checkplots, these dicts must be of the form below, including at least
        the keys indicated here::

            {'periods': np.array of all periods searched by the period-finder,
             'lspvals': np.array of periodogram power value for each period,
             'bestperiod': a float value that is the period with the highest
                           peak in the periodogram, i.e. the most-likely actual
                           period,
             'method': a three-letter code naming the period-finder used; must
                       be one of the keys in the
                       `astrobase.periodbase.METHODLABELS` dict,
             'nbestperiods': a list of the periods corresponding to periodogram
                             peaks (`nbestlspvals` below) to annotate on the
                             periodogram plot so they can be called out
                             visually,
             'nbestlspvals': a list of the power values associated with
                             periodogram peaks to annotate on the periodogram
                             plot so they can be called out visually; should be
                             the same length as `nbestperiods` above}

        `nbestperiods` and `nbestlspvals` in each lspinfo dict must have at
        least as many elements as the `nperiodstouse` kwarg to this function.

    times,mags,errs : np.arrays
        The magnitude/flux time-series to process for this checkplot along with
        their associated measurement errors.

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

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately.

    nperiodstouse : int
        This controls how many 'best' periods to make phased LC plots for. By
        default, this is the 3 best. If this is set to None, all 'best' periods
        present in each lspinfo dict's 'nbestperiods' key will be processed for
        this checkplot.

    objectinfo : dict or None
        If provided, this is a dict containing information on the object whose
        light curve is being processed. This function will then be able to look
        up and download a finder chart for this object and write that to the
        output checkplotdict. External services such as GAIA, SIMBAD, TIC@MAST,
        etc. will also be used to look up this object by its coordinates, and
        will add in information available from those services.

        The `objectinfo` dict must be of the form and contain at least the keys
        described below::

            {'objectid': the name of the object,
             'ra': the right ascension of the object in decimal degrees,
             'decl': the declination of the object in decimal degrees,
             'ndet': the number of observations of this object}

        You can also provide magnitudes and proper motions of the object using
        the following keys and the appropriate values in the `objectinfo`
        dict. These will be used to calculate colors, total and reduced proper
        motion, etc. and display these in the output checkplot PNG::

            'pmra' -> the proper motion in mas/yr in right ascension,
            'pmdecl' -> the proper motion in mas/yr in the declination,
            'umag'  -> U mag		 -> colors: U-B, U-V, U-g
            'bmag'  -> B mag		 -> colors: U-B, B-V
            'vmag'  -> V mag		 -> colors: U-V, B-V, V-R, V-I, V-K
            'rmag'  -> R mag		 -> colors: V-R, R-I
            'imag'  -> I mag		 -> colors: g-I, V-I, R-I, B-I
            'jmag'  -> 2MASS J mag	 -> colors: J-H, J-K, g-J, i-J
            'hmag'  -> 2MASS H mag	 -> colors: J-H, H-K
            'kmag'  -> 2MASS Ks mag	 -> colors: g-Ks, H-Ks, J-Ks, V-Ks
            'sdssu' -> SDSS u mag	 -> colors: u-g, u-V
            'sdssg' -> SDSS g mag	 -> colors: g-r, g-i, g-K, u-g, U-g, g-J
            'sdssr' -> SDSS r mag	 -> colors: r-i, g-r
            'sdssi' -> SDSS i mag	 -> colors: r-i, i-z, g-i, i-J, i-W1
            'sdssz' -> SDSS z mag	 -> colors: i-z, z-W2, g-z
            'ujmag' -> UKIRT J mag	 -> colors: J-H, H-K, J-K, g-J, i-J
            'uhmag' -> UKIRT H mag	 -> colors: J-H, H-K
            'ukmag' -> UKIRT K mag	 -> colors: g-K, H-K, J-K, V-K
            'irac1' -> Spitzer IRAC1 mag -> colors: i-I1, I1-I2
            'irac2' -> Spitzer IRAC2 mag -> colors: I1-I2, I2-I3
            'irac3' -> Spitzer IRAC3 mag -> colors: I2-I3
            'irac4' -> Spitzer IRAC4 mag -> colors: I3-I4
            'wise1' -> WISE W1 mag	 -> colors: i-W1, W1-W2
            'wise2' -> WISE W2 mag	 -> colors: W1-W2, W2-W3
            'wise3' -> WISE W3 mag	 -> colors: W2-W3
            'wise4' -> WISE W4 mag	 -> colors: W3-W4

        If you have magnitude measurements in other bands, use the
        `custom_bandpasses` kwarg to pass these in.

        If this is None, no object information will be incorporated into the
        checkplot (kind of making it effectively useless for anything other than
        glancing at the phased light curves at various 'best' periods from the
        period-finder results).

    deredden_object : bool
        If this is True, will use the 2MASS DUST service to get extinction
        coefficients in various bands, and then try to deredden the magnitudes
        and colors of the object already present in the checkplot's objectinfo
        dict.

    custom_bandpasses : dict
        This is a dict used to provide custom bandpass definitions for any
        magnitude measurements in the objectinfo dict that are not automatically
        recognized by :py:func:`astrobase.varclass.starfeatures.color_features`.

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

    gaia_mirror : str or None
        This sets the GAIA mirror to use. This is a key in the
        `services.gaia.GAIA_URLS` dict which defines the URLs to hit for each
        mirror.

    complete_query_later : bool
        If this is True, saves the state of GAIA queries that are not yet
        complete when `gaia_max_timeout` is reached while waiting for the GAIA
        service to respond to our request. A later call for GAIA info on the
        same object will attempt to pick up the results from the existing query
        if it's completed. If `fast_mode` is True, this is ignored.

    varinfo : dict
        If this is None, a blank dict of the form below will be added to the
        checkplotdict::

            {'objectisvar': None -> variability flag (None indicates unset),
             'vartags': CSV str containing variability type tags from review,
             'varisperiodic': None -> periodic variability flag (None -> unset),
             'varperiod': the period associated with the periodic variability,
             'varepoch': the epoch associated with the periodic variability}

        If you provide a dict matching this format in this kwarg, this will be
        passed unchanged to the output checkplotdict produced.

    getvarfeatures : bool
        If this is True, several light curve variability features for this
        object will be calculated and added to the output checkpotdict as
        checkplotdict['varinfo']['features']. This uses the function
        `varclass.varfeatures.all_nonperiodic_features` so see its docstring for
        the measures that are calculated (e.g. Stetson J indices, dispersion
        measures, etc.)

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

    nbrradiusarcsec : flaot
        The radius in arcseconds to use for a search conducted around the
        coordinates of this object to look for any potential confusion and
        blending of variability amplitude caused by their proximity.

    maxnumneighbors : int
        The maximum number of neighbors that will have their light curves and
        magnitudes noted in this checkplot as potential blends with the target
        object.

    xmatchinfo : str or dict
        This is either the xmatch dict produced by the function
        `load_xmatch_external_catalogs` above, or the path to the xmatch info
        pickle file produced by that function.

    xmatchradiusarcsec : float
        This is the cross-matching radius to use in arcseconds.

    lcfitfunc : Python function or None
        If provided, this should be a Python function that is used to fit a
        model to the light curve. This fit is then overplotted for each phased
        light curve in the checkplot. This function should have the following
        signature:

        `def lcfitfunc(times, mags, errs, period, **lcfitparams)`

        where `lcfitparams` encapsulates all external parameters (i.e. number of
        knots for a spline function, the degree of a Legendre polynomial fit,
        etc., planet transit parameters) This function should return a Python
        dict with the following structure (similar to the functions in
        `astrobase.lcfit`) and at least the keys below::

            {'fittype':<str: name of fit method>,
             'fitchisq':<float: the chi-squared value of the fit>,
             'fitredchisq':<float: the reduced chi-squared value of the fit>,
             'fitinfo':{'fitmags':<ndarray: model mags/fluxes from fit func>},
             'magseries':{'times':<ndarray: times where fitmags are evaluated>}}

        Additional keys in the dict returned from this function can include
        `fitdict['fitinfo']['finalparams']` for the final model fit parameters
        (this will be used by the checkplotserver if present),
        `fitdict['fitinfo']['fitepoch']` for the minimum light epoch returned by
        the model fit, among others.

        In any case, the output dict of `lcfitfunc` will be copied to the output
        checkplotdict as
        `checkplotdict[lspmethod][periodind]['lcfit'][<fittype>]` for each
        phased light curve.

    lcfitparams : dict
        A dict containing the LC fit parameters to use when calling the function
        provided in `lcfitfunc`. This contains key-val pairs corresponding to
        parameter names and their respective initial values to be used by the
        fit function.

    externalplots : list of tuples of str
        If provided, this is a list of 4-element tuples containing:

        1. path to PNG of periodogram from an external period-finding method
        2. path to PNG of best period phased LC from the external period-finder
        3. path to PNG of 2nd-best phased LC from the external period-finder
        4. path to PNG of 3rd-best phased LC from the external period-finder

        This can be used to incorporate external period-finding method results
        into the output checkplot pickle or exported PNG to allow for comparison
        with astrobase results. Example of `externalplots`::

            [('/path/to/external/bls-periodogram.png',
              '/path/to/external/bls-phasedlc-plot-bestpeak.png',
              '/path/to/external/bls-phasedlc-plot-peak2.png',
              '/path/to/external/bls-phasedlc-plot-peak3.png'),
             ('/path/to/external/pdm-periodogram.png',
              '/path/to/external/pdm-phasedlc-plot-bestpeak.png',
              '/path/to/external/pdm-phasedlc-plot-peak2.png',
              '/path/to/external/pdm-phasedlc-plot-peak3.png'),
             ...]

        If `externalplots` is provided here, these paths will be stored in the
        output checkplotdict. The `checkplot.pkl_png.checkplot_pickle_to_png`
        function can then automatically retrieve these plot PNGs and put
        them into the exported checkplot PNG.

    findercmap : str or matplotlib.cm.ColorMap object
        The Colormap object to use for the finder chart image.

    finderconvolve : astropy.convolution.Kernel object or None
        If not None, the Kernel object to use for convolving the finder image.

    findercachedir : str
        The path to the astrobase cache directory for finder chart downloads
        from the NASA SkyView service.

    normto : {'globalmedian', 'zero'} or a float
        This specifies the normalization target::

            'globalmedian' -> norms each mag to global median of the LC column
            'zero'         -> norms each mag to zero
            a float        -> norms each mag to this specified float value.

    normmingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

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

    varepoch : 'min' or float or list of lists or None
        The epoch to use for this phased light curve plot tile. If this is a
        float, will use the provided value directly. If this is 'min', will
        automatically figure out the time-of-minimum of the phased light
        curve. If this is None, will use the mimimum value of `stimes` as the
        epoch of the phased light curve plot. If this is a list of lists, will
        use the provided value of `lspmethodind` to look up the current
        period-finder method and the provided value of `periodind` to look up
        the epoch associated with that method and the current period. This is
        mostly only useful when `twolspmode` is True.

    phasewrap : bool
        If this is True, the phased time-series will be wrapped around
        phase 0.0.

    phasesort : bool
        If True, will sort the phased light curve in order of increasing phase.

    phasebin: float
        The bin size to use to group together measurements closer than this
        amount in phase. This is in units of phase. If this is a float, a
        phase-binned version of the phased light curve will be overplotted on
        top of the regular phased light curve.

    minbinelems : int
        The minimum number of elements required per phase bin to include it in
        the phased LC plot.

    plotxlim : sequence of two floats or None
        The x-range (min, max) of the phased light curve plot. If None, will be
        determined automatically.

    xliminsetmode : bool
        If this is True, the generated phased light curve plot will use the
        values of `plotxlim` as the main plot x-axis limits (i.e. zoomed-in if
        `plotxlim` is a range smaller than the full phase range), and will show
        the full phased light curve plot as an smaller inset. Useful for
        planetary transit light curves.

    plotdpi : int
        The resolution of the output plot PNGs in dots per inch.

    bestperiodhighlight : str or None
        If not None, this is a str with a matplotlib color specification to use
        as the background color to highlight the phased light curve plot of the
        'best' period and epoch combination. If None, no highlight will be
        applied.

    xgridlines : list of floats or None
        If this is provided, must be a list of floats corresponding to the phase
        values where to draw vertical dashed lines as a means of highlighting
        these.

    mindet : int
        The minimum of observations the input object's mag/flux time-series must
        have for this function to plot its light curve and phased light
        curve. If the object has less than this number, no light curves will be
        plotted, but the checkplotdict will still contain all of the other
        information.

    verbose : bool
        If True, will indicate progress and warn about problems.

    outfile : str or None
        The name of the output checkplot pickle file. If this is None, will
        write the checkplot pickle to file called 'checkplot.pkl' in the current
        working directory.

    outgzip : bool
        This controls whether to gzip the output pickle. It turns out that this
        is the slowest bit in the output process, so if you're after speed, best
        not to use this. This is False by default since it turns out that gzip
        actually doesn't save that much space (29 MB vs. 35 MB for the average
        checkplot pickle).

    pickleprotocol : int or None
        This sets the pickle file protocol to use when writing the pickle:

        If None, will choose a protocol using the following rules:

        - 4 -> default in Python >= 3.4 - fast but incompatible with Python 2
        - 3 -> default in Python 3.0-3.3 - mildly fast
        - 2 -> default in Python 2 - very slow, but compatible with Python 2/3

        The default protocol kwarg is None, this will make an automatic choice
        for pickle protocol that's best suited for the version of Python in
        use. Note that this will make pickles generated by Py3 incompatible with
        Py2.

    returndict : bool
        If this is True, will return the checkplotdict instead of returning the
        filename of the output checkplot pickle.

    Returns
    -------

    dict or str
        If returndict is False, will return the path to the generated checkplot
        pickle file. If returndict is True, will return the checkplotdict
        instead.

    '''

    # call checkplot_dict for most of the work
    checkplotdict = checkplot_dict(
        lspinfolist,
        times,
        mags,
        errs,
        magsarefluxes=magsarefluxes,
        nperiodstouse=nperiodstouse,
        objectinfo=objectinfo,
        deredden_object=deredden_object,
        custom_bandpasses=custom_bandpasses,
        gaia_submit_timeout=gaia_submit_timeout,
        gaia_submit_tries=gaia_submit_tries,
        gaia_max_timeout=gaia_max_timeout,
        gaia_mirror=gaia_mirror,
        complete_query_later=complete_query_later,
        varinfo=varinfo,
        getvarfeatures=getvarfeatures,
        lclistpkl=lclistpkl,
        nbrradiusarcsec=nbrradiusarcsec,
        maxnumneighbors=maxnumneighbors,
        xmatchinfo=xmatchinfo,
        xmatchradiusarcsec=xmatchradiusarcsec,
        lcfitfunc=lcfitfunc,
        lcfitparams=lcfitparams,
        externalplots=externalplots,
        findercmap=findercmap,
        finderconvolve=finderconvolve,
        findercachedir=findercachedir,
        normto=normto,
        normmingap=normmingap,
        sigclip=sigclip,
        varepoch=varepoch,
        phasewrap=phasewrap,
        phasesort=phasesort,
        phasebin=phasebin,
        minbinelems=minbinelems,
        plotxlim=plotxlim,
        xliminsetmode=xliminsetmode,
        plotdpi=plotdpi,
        bestperiodhighlight=bestperiodhighlight,
        xgridlines=xgridlines,
        mindet=mindet,
        verbose=verbose,
        fast_mode=fast_mode
    )

    # for Python >= 3.4, use v4
    if ((sys.version_info[0:2] >= (3,4) and not pickleprotocol) or
        (pickleprotocol > 2)):
        pickleprotocol = 4

    elif ((sys.version_info[0:2] >= (3,0) and not pickleprotocol) or
          (pickleprotocol > 2)):
        pickleprotocol = 3

    # for Python == 2.7; use v2
    elif sys.version_info[0:2] == (2,7) and not pickleprotocol:
        pickleprotocol = 2

    # otherwise, if left unspecified, use the slowest but most compatible
    # protocol. this will be readable by all (most?) Pythons
    elif not pickleprotocol:
        pickleprotocol = 0


    # generate the output file path
    if outgzip:

        # generate the outfile filename
        if (not outfile and
            len(lspinfolist) > 0 and
            isinstance(lspinfolist[0], str)):
            plotfpath = os.path.join(os.path.dirname(lspinfolist[0]),
                                     'checkplot-%s.pkl.gz' %
                                     checkplotdict['objectid'])
        elif outfile:
            plotfpath = outfile
        else:
            plotfpath = 'checkplot.pkl.gz'

    else:

        # generate the outfile filename
        if (not outfile and
            len(lspinfolist) > 0 and
            isinstance(lspinfolist[0], str)):
            plotfpath = os.path.join(os.path.dirname(lspinfolist[0]),
                                     'checkplot-%s.pkl' %
                                     checkplotdict['objectid'])
        elif outfile:
            plotfpath = outfile
        else:
            plotfpath = 'checkplot.pkl'


    # write the completed checkplotdict to a gzipped pickle
    picklefname = _write_checkplot_picklefile(checkplotdict,
                                              outfile=plotfpath,
                                              protocol=pickleprotocol,
                                              outgzip=outgzip)

    # at the end, return the dict and filename if asked for
    if returndict:
        if verbose:
            LOGINFO('checkplot done -> %s' % picklefname)
        return checkplotdict, picklefname

    # otherwise, just return the filename
    else:
        # just to make sure: free up space
        del checkplotdict
        if verbose:
            LOGINFO('checkplot done -> %s' % picklefname)
        return picklefname