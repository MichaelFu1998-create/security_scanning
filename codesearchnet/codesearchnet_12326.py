def twolsp_checkplot_png(lspinfo1,
                         lspinfo2,
                         times,
                         mags,
                         errs,
                         varepoch='min',
                         magsarefluxes=False,
                         objectinfo=None,
                         findercmap='gray_r',
                         finderconvolve=None,
                         findercachedir='~/.astrobase/stamp-cache',
                         normto='globalmedian',
                         normmingap=4.0,
                         sigclip=4.0,
                         phasewrap=True,
                         phasesort=True,
                         phasebin=0.002,
                         minbinelems=7,
                         plotxlim=(-0.8,0.8),
                         unphasedms=2.0,
                         phasems=2.0,
                         phasebinms=4.0,
                         xliminsetmode=False,
                         bestperiodhighlight=None,
                         plotdpi=100,
                         outfile=None,
                         verbose=True):
    '''This makes a checkplot using results from two independent period-finders.

    Adapted from Luke Bouma's implementation of a similar function in his
    work. This makes a special checkplot that uses two lspinfo dictionaries,
    from two independent period-finding methods. For EBs, it's probably best to
    use Stellingwerf PDM or Schwarzenberg-Czerny AoV as one of these, and the
    Box Least-squared Search method as the other one.

    The checkplot layout in this case is::

        [ pgram1 + objectinfo ] [        pgram2       ] [     unphased LC     ]
        [ pgram1 P1 phased LC ] [ pgram1 P2 phased LC ] [ pgram1 P3 phased LC ]
        [ pgram2 P1 phased LC ] [ pgram2 P2 phased LC ] [ pgram2 P3 phased LC ]

    where:

    - pgram1 is the plot for the periodogram in the lspinfo1 dict
    - pgram1 P1, P2, and P3 are the best three periods from lspinfo1
    - pgram2 is the plot for the periodogram in the lspinfo2 dict
    - pgram2 P1, P2, and P3 are the best three periods from lspinfo2

    Note that we take the output file name from lspinfo1 if lspinfo1 is a string
    filename pointing to a (gzipped) pickle containing the results dict from a
    period-finding routine similar to those in periodbase.

    Parameters
    ----------

    lspinfo1,lspinfo2 : dict or str
        If this is a dict, it must be a dict produced by an
        `astrobase.periodbase` period-finder function or a dict from your own
        period-finder function or routine that is of the form below with at
        least these keys::

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

        `nbestperiods` and `nbestlspvals` must have at least 3 elements each,
        e.g. describing the three 'best' (highest power) peaks in the
        periodogram.

        If lspinfo is a str, then it must be a path to a pickle file (ending
        with the extension '.pkl' or '.pkl.gz') that contains a dict of the form
        described above.

    times,mags,errs : np.array
        The mag/flux time-series arrays to process along with associated errors.

    varepoch : 'min' or float or None or list of lists
        This sets the time of minimum light finding strategy for the checkplot::

                                                   the epoch used for all phased
            If `varepoch` is None               -> light curve plots will be
                                                   `min(times)`.

            If `varepoch='min'`                 -> automatic epoch finding for all
                                                   periods using light curve fits.

            If varepoch is a single float       -> this epoch will be used for all
                                                   phased light curve plots

            If varepoch is a list of floats        each epoch will be applied to
            with length = `len(nbestperiods)` ->   the phased light curve for each
            from period-finder results             period specifically

        If you use a list for varepoch, it must be of length
        `len(lspinfo['nbestperiods'])`.

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately/

    objectinfo : dict or None
        If provided, this is a dict containing information on the object whose
        light curve is being processed. This function will then be able to look
        up and download a finder chart for this object and write that to the
        output checkplot PNG image.The `objectinfo` dict must be of the form and
        contain at least the keys described below::

            {'objectid': the name of the object,
             'ra': the right ascension of the object in decimal degrees,
             'decl': the declination of the object in decimal degrees,
             'ndet': the number of observations of this object}

        You can also provide magnitudes and proper motions of the object using
        the following keys and the appropriate values in the `objectinfo`
        dict. These will be used to calculate colors, total and reduced proper
        motion, etc. and display these in the output checkplot PNG.

        - SDSS mag keys: 'sdssu', 'sdssg', 'sdssr', 'sdssi', 'sdssz'
        - 2MASS mag keys: 'jmag', 'hmag', 'kmag'
        - Cousins mag keys: 'bmag', 'vmag'
        - GAIA specific keys: 'gmag', 'teff'
        - proper motion keys: 'pmra', 'pmdecl'

    findercmap : str or matplotlib.cm.ColorMap object
        The Colormap object to use for the finder chart image.

    finderconvolve : astropy.convolution.Kernel object or None
        If not None, the Kernel object to use for convolving the finder image.

    findercachedir : str
        The directory where the FITS finder images are downloaded and cached.

    normto : {'globalmedian', 'zero'} or a float
        This sets the LC normalization target::

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

    phasewrap : bool
        If this is True, the phased time-series will be wrapped around phase
        0.0.

    phasesort : bool
        If this is True, the phased time-series will be sorted in phase.

    phasebin : float or None
        If this is provided, indicates the bin size to use to group together
        measurements closer than this amount in phase. This is in units of
        phase. The binned phased light curve will be overplotted on top of the
        phased light curve. Useful for when one has many measurement points and
        needs to pick out a small trend in an otherwise noisy phased light
        curve.

    minbinelems : int
        The minimum number of elements in each phase bin.

    plotxlim : sequence of two floats or None
        The x-axis limits to use when making the phased light curve plot. By
        default, this is (-0.8, 0.8), which places phase 0.0 at the center of
        the plot and covers approximately two cycles in phase to make any trends
        clear.

    unphasedms : float
        The marker size to use for the main unphased light curve plot symbols.

    phasems : float
        The marker size to use for the main phased light curve plot symbols.

    phasebinms : float
        The marker size to use for the binned phased light curve plot symbols.

    xliminsetmode : bool
        If this is True, the generated phased light curve plot will use the
        values of `plotxlim` as the main plot x-axis limits (i.e. zoomed-in if
        `plotxlim` is a range smaller than the full phase range), and will show
        the full phased light curve plot as an smaller inset. Useful for
        planetary transit light curves.

    bestperiodhighlight : str or None
        If not None, this is a str with a matplotlib color specification to use
        as the background color to highlight the phased light curve plot of the
        'best' period and epoch combination. If None, no highlight will be
        applied.

    outfile : str or None
        The file name of the file to save the checkplot to. If this is None,
        will write to a file called 'checkplot.png' in the current working
        directory.

    plotdpi : int
        Sets the resolution in DPI for PNG plots (default = 100).

    verbose : bool
        If False, turns off many of the informational messages. Useful for
        when an external function is driving lots of `checkplot_png` calls.

    Returns
    -------

    str
        The file path to the generated checkplot PNG file.

    '''

    # generate the plot filename
    if not outfile and isinstance(lspinfo1,str):
        plotfpath = os.path.join(
            os.path.dirname(lspinfo1),
            'twolsp-checkplot-%s.png' % (
                os.path.basename(lspinfo1),
            )
        )
    elif outfile:
        plotfpath = outfile
    else:
        plotfpath = 'twolsp-checkplot.png'

    # get the first LSP from a pickle file transparently
    if isinstance(lspinfo1,str) and os.path.exists(lspinfo1):
        if verbose:
            LOGINFO('loading LSP info from pickle %s' % lspinfo1)

        if '.gz' in lspinfo1:
            with gzip.open(lspinfo1,'rb') as infd:
                lspinfo1 = pickle.load(infd)
        else:
            with open(lspinfo1,'rb') as infd:
                lspinfo1 = pickle.load(infd)


    # get the second LSP from a pickle file transparently
    if isinstance(lspinfo2,str) and os.path.exists(lspinfo2):
        if verbose:
            LOGINFO('loading LSP info from pickle %s' % lspinfo2)

        if '.gz' in lspinfo2:
            with gzip.open(lspinfo2,'rb') as infd:
                lspinfo2 = pickle.load(infd)
        else:
            with open(lspinfo2,'rb') as infd:
                lspinfo2 = pickle.load(infd)


    # get the things to plot out of the data
    if ('periods' in lspinfo1 and 'periods' in lspinfo2 and
        'lspvals' in lspinfo1 and 'lspvals' in lspinfo2 and
        'bestperiod' in lspinfo1 and 'bestperiod' in lspinfo2):

        bestperiod1 = lspinfo1['bestperiod']
        nbestperiods1 = lspinfo1['nbestperiods']
        lspmethod1 = lspinfo1['method']

        bestperiod2 = lspinfo2['bestperiod']
        nbestperiods2 = lspinfo2['nbestperiods']
        lspmethod2 = lspinfo2['method']

    else:

        LOGERROR('could not understand lspinfo1 or lspinfo2 '
                 'for this object, skipping...')
        return None


    if (not npisfinite(bestperiod1)) or (not npisfinite(bestperiod2)):

        LOGWARNING('no best period found for this object, skipping...')
        return None

    # initialize the plot
    fig, axes = plt.subplots(3,3)
    axes = npravel(axes)

    # this is a full page plot
    fig.set_size_inches(30,24)

    ######################################################################
    ## PLOT 1 is the LSP from lspinfo1, including objectinfo and finder ##
    ######################################################################

    _make_periodogram(axes[0], lspinfo1, objectinfo,
                      findercmap, finderconvolve,
                      verbose=verbose,
                      findercachedir=findercachedir)

    #####################################
    ## PLOT 2 is the LSP from lspinfo2 ##
    #####################################

    _make_periodogram(axes[1], lspinfo2, None,
                      findercmap, finderconvolve)

    ##########################################
    ## FIX UP THE MAGS AND REMOVE BAD STUFF ##
    ##########################################

    # sigclip first
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # take care of the normalization
    if normto is not False:
        stimes, smags = normalize_magseries(stimes, smags,
                                            normto=normto,
                                            magsarefluxes=magsarefluxes,
                                            mingap=normmingap)


    # make sure we have some lightcurve points to plot after sigclip
    if len(stimes) >= 50:

        ##############################
        ## PLOT 3 is an unphased LC ##
        ##############################

        _make_magseries_plot(axes[2], stimes, smags, serrs,
                             magsarefluxes=magsarefluxes,
                             ms=unphasedms)

        # make the plot for each best period
        lspbestperiods1 = nbestperiods1[::]
        lspbestperiods2 = nbestperiods2[::]

        ##########################################################
        ### NOW PLOT PHASED LCS FOR 3 BEST PERIODS IN LSPINFO1 ###
        ##########################################################
        for periodind, varperiod, plotaxes in zip([0,1,2],
                                                  lspbestperiods1[:3],
                                                  [axes[3], axes[4], axes[5]]):


            # make sure the best period phased LC plot stands out
            if periodind == 0 and bestperiodhighlight:
                if MPLVERSION >= (2,0,0):
                    plotaxes.set_facecolor(bestperiodhighlight)
                else:
                    plotaxes.set_axis_bgcolor(bestperiodhighlight)

            _make_phased_magseries_plot(plotaxes,
                                        periodind,
                                        stimes, smags, serrs,
                                        varperiod, varepoch,
                                        phasewrap, phasesort,
                                        phasebin, minbinelems,
                                        plotxlim, lspmethod1,
                                        lspmethodind=0,
                                        twolspmode=True,
                                        magsarefluxes=magsarefluxes,
                                        xliminsetmode=xliminsetmode,
                                        verbose=verbose,
                                        phasems=phasems,
                                        phasebinms=phasebinms)

        ##########################################################
        ### NOW PLOT PHASED LCS FOR 3 BEST PERIODS IN LSPINFO2 ###
        ##########################################################
        for periodind, varperiod, plotaxes in zip([0,1,2],
                                                  lspbestperiods2[:3],
                                                  [axes[6], axes[7], axes[8]]):


            # make sure the best period phased LC plot stands out
            if periodind == 0 and bestperiodhighlight:
                if MPLVERSION >= (2,0,0):
                    plotaxes.set_facecolor(bestperiodhighlight)
                else:
                    plotaxes.set_axis_bgcolor(bestperiodhighlight)

            _make_phased_magseries_plot(plotaxes,
                                        periodind,
                                        stimes, smags, serrs,
                                        varperiod, varepoch,
                                        phasewrap, phasesort,
                                        phasebin, minbinelems,
                                        plotxlim, lspmethod2,
                                        lspmethodind=1,
                                        twolspmode=True,
                                        magsarefluxes=magsarefluxes,
                                        xliminsetmode=xliminsetmode,
                                        verbose=verbose,
                                        phasems=phasems,
                                        phasebinms=phasebinms)

        # end of plotting for each ax

        # save the plot to disk
        fig.set_tight_layout(True)
        if plotfpath.endswith('.png'):
            fig.savefig(plotfpath,dpi=plotdpi)
        else:
            fig.savefig(plotfpath)
        plt.close()

        if verbose:
            LOGINFO('checkplot done -> %s' % plotfpath)
        return plotfpath

    # otherwise, there's no valid data for this plot
    else:

        LOGWARNING('no good data')

        for periodind in range(5):

            axes[periodind+2].text(
                0.5,0.5,
                ('no best aperture light curve available'),
                horizontalalignment='center',
                verticalalignment='center',
                transform=axes[periodind+2].transAxes
            )

        fig.set_tight_layout(True)

        if plotfpath.endswith('.png'):
            fig.savefig(plotfpath, dpi=plotdpi)
        else:
            fig.savefig(plotfpath)

        plt.close()

        if verbose:
            LOGINFO('checkplot done -> %s' % plotfpath)
        return plotfpath