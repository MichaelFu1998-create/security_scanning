def _pkl_phased_magseries_plot(
        checkplotdict,
        lspmethod,
        periodind,
        stimes, smags, serrs,
        varperiod, varepoch,
        lspmethodind=0,
        phasewrap=True,
        phasesort=True,
        phasebin=0.002,
        minbinelems=7,
        plotxlim=(-0.8,0.8),
        plotdpi=100,
        bestperiodhighlight=None,
        xgridlines=None,
        xliminsetmode=False,
        magsarefluxes=False,
        directreturn=False,
        overplotfit=None,
        verbose=True,
        override_pfmethod=None
):
    '''This returns the phased magseries plot PNG as base64 plus info as a dict.

    Parameters
    ----------

    checkplotdict : dict
        This is an existing checkplotdict to update. If it's None or
        `directreturn` = True, then the generated dict result for this magseries
        plot will be returned directly.

    lspmethod : str
        lspmethod is a string indicating the type of period-finding algorithm
        that produced the period. If this is not in
        `astrobase.plotbase.METHODSHORTLABELS`, it will be used verbatim. In
        most cases, this will come directly from the lspinfo dict produced by a
        period-finder function.

    periodind : int
        This is the index of the current periodogram period being operated
        on::

            If == 0 -> best period and `bestperiodhighlight` is applied if not
                       None
            If > 0   -> some other peak of the periodogram
            If == -1 -> special mode w/ no periodogram labels and enabled
                        highlight

    stimes,smags,serrs : np.array
        The mag/flux time-series arrays along with associated errors. These
        should all have been run through nan-stripping and sigma-clipping
        beforehand.

    varperiod : float or None
        The period to use for this phased light curve plot tile.

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

    xliminsetmode : bool
        If this is True, the generated phased light curve plot will use the
        values of `plotxlim` as the main plot x-axis limits (i.e. zoomed-in if
        `plotxlim` is a range smaller than the full phase range), and will show
        the full phased light curve plot as an smaller inset. Useful for
        planetary transit light curves.

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately.

    directreturn : bool
        If this set to True, will return only the dict corresponding to the
        phased LC plot for the input `periodind` and `lspmethod` and not return
        this result embedded in a checkplotdict.

    overplotfit : dict
        If this is provided, it must be a dict of the form returned by one of
        the astrobase.lcfit.fit_XXXXX_magseries functions. This can be used to
        overplot a light curve model fit on top of the phased light curve plot
        returned by this function. The `overplotfit` dict has the following
        form, including at least the keys listed here::

            {'fittype':str: name of fit method,
            'fitchisq':float: the chi-squared value of the fit,
            'fitredchisq':float: the reduced chi-squared value of the fit,
            'fitinfo':{'fitmags':array: model mags or fluxes from fit function},
            'magseries':{'times':array: times where the fitmags are evaluated}}

        `fitmags` and `times` should all be of the same size. The input
        `overplotfit` dict is copied over to the checkplotdict for each specific
        phased LC plot to save all of this information for use later.

    verbose : bool
        If True, will indicate progress and warn about problems.

    override_pfmethod : str or None
        This is used to set a custom label for the periodogram method. Normally,
        this is taken from the 'method' key in the input `lspinfo` dict, but if
        you want to override the output method name, provide this as a string
        here. This can be useful if you have multiple results you want to
        incorporate into a checkplotdict from a single period-finder (e.g. if
        you ran BLS over several period ranges separately).

    Returns
    -------

    dict
        Returns a dict of the following form::

            {lspmethod: {'plot': the phased LC plot as base64 str,
                         'period': the period used for this phased LC,
                         'epoch': the epoch used for this phased LC,
                         'phase': phase value array,
                         'phasedmags': mags/fluxes sorted in phase order,
                         'binphase': array of binned phase values,
                         'binphasedmags': mags/fluxes sorted in binphase order,
                         'phasewrap': value of the input `phasewrap` kwarg,
                         'phasesort': value of the input `phasesort` kwarg,
                         'phasebin': value of the input `phasebin` kwarg,
                         'minbinelems': value of the input `minbinelems` kwarg,
                         'plotxlim': value of the input `plotxlim` kwarg,
                         'lcfit': the provided `overplotfit` dict}}

        The dict is in this form because we can use Python dicts' `update()`
        method to update an existing checkplotdict. If `returndirect` is True,
        only the inner dict is returned.

    '''

    # open the figure instance
    phasedseriesfig = plt.figure(figsize=(7.5,4.8),dpi=plotdpi)

    plotvarepoch = None

    # figure out the epoch, if it's None, use the min of the time
    if varepoch is None:
        plotvarepoch = npmin(stimes)

    # if the varepoch is 'min', then fit a spline to the light curve
    # phased using the min of the time, find the fit mag minimum and use
    # the time for that as the varepoch
    elif isinstance(varepoch,str) and varepoch == 'min':

        try:
            spfit = spline_fit_magseries(stimes,
                                         smags,
                                         serrs,
                                         varperiod,
                                         magsarefluxes=magsarefluxes,
                                         sigclip=None,
                                         verbose=verbose)
            plotvarepoch = spfit['fitinfo']['fitepoch']
            if len(plotvarepoch) != 1:
                plotvarepoch = plotvarepoch[0]


        except Exception as e:

            LOGERROR('spline fit failed, trying SavGol fit')

            sgfit = savgol_fit_magseries(stimes,
                                         smags,
                                         serrs,
                                         varperiod,
                                         sigclip=None,
                                         magsarefluxes=magsarefluxes,
                                         verbose=verbose)
            plotvarepoch = sgfit['fitinfo']['fitepoch']
            if len(plotvarepoch) != 1:
                plotvarepoch = plotvarepoch[0]

        finally:

            if plotvarepoch is None:

                LOGERROR('could not find a min epoch time, '
                         'using min(times) as the epoch for '
                         'the phase-folded LC')

                plotvarepoch = npmin(stimes)

    # special case with varepoch lists per each period-finder method
    elif isinstance(varepoch, list):

        try:
            thisvarepochlist = varepoch[lspmethodind]
            plotvarepoch = thisvarepochlist[periodind]
        except Exception as e:
            LOGEXCEPTION(
                "varepoch provided in list form either doesn't match "
                "the length of nbestperiods from the period-finder "
                "result, or something else went wrong. using min(times) "
                "as the epoch instead"
            )
            plotvarepoch = npmin(stimes)

    # the final case is to use the provided varepoch directly
    else:
        plotvarepoch = varepoch


    if verbose:
        LOGINFO('plotting %s phased LC with period %s: %.6f, epoch: %.5f' %
                (lspmethod, periodind, varperiod, plotvarepoch))

    # make the plot title based on the lspmethod
    if periodind == 0:
        plottitle = '%s best period: %.6f d - epoch: %.5f' % (
            (METHODSHORTLABELS[lspmethod] if lspmethod in METHODSHORTLABELS
             else lspmethod),
            varperiod,
            plotvarepoch
        )
    elif periodind > 0:
        plottitle = '%s peak %s: %.6f d - epoch: %.5f' % (
            (METHODSHORTLABELS[lspmethod] if lspmethod in METHODSHORTLABELS
             else lspmethod),
            periodind+1,
            varperiod,
            plotvarepoch
        )
    elif periodind == -1:
        plottitle = '%s period: %.6f d - epoch: %.5f' % (
            lspmethod,
            varperiod,
            plotvarepoch
        )


    # phase the magseries
    phasedlc = phase_magseries(stimes,
                               smags,
                               varperiod,
                               plotvarepoch,
                               wrap=phasewrap,
                               sort=phasesort)
    plotphase = phasedlc['phase']
    plotmags = phasedlc['mags']

    # if we're supposed to bin the phases, do so
    if phasebin:

        binphasedlc = phase_bin_magseries(plotphase,
                                          plotmags,
                                          binsize=phasebin,
                                          minbinelems=minbinelems)
        binplotphase = binphasedlc['binnedphases']
        binplotmags = binphasedlc['binnedmags']

    else:
        binplotphase = None
        binplotmags = None


    # finally, make the phased LC plot
    plt.plot(plotphase,
             plotmags,
             marker='o',
             ms=2.0, ls='None',mew=0,
             color='gray',
             rasterized=True)

    # overlay the binned phased LC plot if we're making one
    if phasebin:
        plt.plot(binplotphase,
                 binplotmags,
                 marker='o',
                 ms=4.0, ls='None',mew=0,
                 color='#1c1e57',
                 rasterized=True)


    # if we're making a overplotfit, then plot the fit over the other stuff
    if overplotfit and isinstance(overplotfit, dict):

        fitmethod = overplotfit['fittype']
        fitredchisq = overplotfit['fitredchisq']

        plotfitmags = overplotfit['fitinfo']['fitmags']
        plotfittimes = overplotfit['magseries']['times']

        # phase the fit magseries
        fitphasedlc = phase_magseries(plotfittimes,
                                      plotfitmags,
                                      varperiod,
                                      plotvarepoch,
                                      wrap=phasewrap,
                                      sort=phasesort)
        plotfitphase = fitphasedlc['phase']
        plotfitmags = fitphasedlc['mags']

        plotfitlabel = (r'%s fit ${\chi}^2/{\mathrm{dof}} = %.3f$' %
                        (fitmethod, fitredchisq))

        # plot the fit phase and mags
        plt.plot(plotfitphase, plotfitmags,'k-',
                 linewidth=3, rasterized=True,label=plotfitlabel)

        plt.legend(loc='upper left', frameon=False)

    # flip y axis for mags
    if not magsarefluxes:
        plot_ylim = plt.ylim()
        plt.ylim((plot_ylim[1], plot_ylim[0]))

    # set the x axis limit
    if not plotxlim:
        plt.xlim((npmin(plotphase)-0.1,
                  npmax(plotphase)+0.1))
    else:
        plt.xlim((plotxlim[0],plotxlim[1]))

    # make a grid
    ax = plt.gca()
    if isinstance(xgridlines, (list, tuple)):
        ax.set_xticks(xgridlines, minor=False)

    plt.grid(color='#a9a9a9',
             alpha=0.9,
             zorder=0,
             linewidth=1.0,
             linestyle=':')


    # make the x and y axis labels
    plot_xlabel = 'phase'
    if magsarefluxes:
        plot_ylabel = 'flux'
    else:
        plot_ylabel = 'magnitude'

    plt.xlabel(plot_xlabel)
    plt.ylabel(plot_ylabel)

    # fix the yaxis ticks (turns off offset and uses the full
    # value of the yaxis tick)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

    # set the plot title
    plt.title(plottitle)

    # make sure the best period phased LC plot stands out
    if (periodind == 0 or periodind == -1) and bestperiodhighlight:
        if MPLVERSION >= (2,0,0):
            plt.gca().set_facecolor(bestperiodhighlight)
        else:
            plt.gca().set_axis_bgcolor(bestperiodhighlight)

    # if we're making an inset plot showing the full range
    if (plotxlim and isinstance(plotxlim, (list, tuple)) and
        len(plotxlim) == 2 and xliminsetmode is True):

        # bump the ylim of the plot so that the inset can fit in this axes plot
        axesylim = plt.gca().get_ylim()

        if magsarefluxes:
            plt.gca().set_ylim(
                axesylim[0],
                axesylim[1] + 0.5*npabs(axesylim[1]-axesylim[0])
            )
        else:
            plt.gca().set_ylim(
                axesylim[0],
                axesylim[1] - 0.5*npabs(axesylim[1]-axesylim[0])
            )

        # put the inset axes in
        inset = inset_axes(plt.gca(), width="40%", height="40%", loc=1)

        # make the scatter plot for the phased LC plot
        inset.plot(plotphase,
                   plotmags,
                   marker='o',
                   ms=2.0, ls='None',mew=0,
                   color='gray',
                   rasterized=True)

        if phasebin:
            # make the scatter plot for the phased LC plot
            inset.plot(binplotphase,
                       binplotmags,
                       marker='o',
                       ms=4.0, ls='None',mew=0,
                       color='#1c1e57',
                       rasterized=True)

        # show the full phase coverage
        if phasewrap:
            inset.set_xlim(-0.2,0.8)
        else:
            inset.set_xlim(-0.1,1.1)

        # flip y axis for mags
        if not magsarefluxes:
            inset_ylim = inset.get_ylim()
            inset.set_ylim((inset_ylim[1], inset_ylim[0]))

        # set the plot title
        inset.text(0.5,0.9,'full phased light curve',
                   ha='center',va='center',transform=inset.transAxes)
        # don't show axes labels or ticks
        inset.set_xticks([])
        inset.set_yticks([])

    # this is the output instance
    phasedseriespng = StrIO()
    phasedseriesfig.savefig(phasedseriespng,
                            # bbox_inches='tight',
                            pad_inches=0.0, format='png')
    plt.close()

    # encode the finderpng instance to base64
    phasedseriespng.seek(0)
    phasedseriesb64 = base64.b64encode(phasedseriespng.read())

    # close the stringio buffer
    phasedseriespng.close()

    # this includes a fitinfo dict if one is provided in overplotfit
    retdict = {
        'plot':phasedseriesb64,
        'period':varperiod,
        'epoch':plotvarepoch,
        'phase':plotphase,
        'phasedmags':plotmags,
        'binphase':binplotphase,
        'binphasedmags':binplotmags,
        'phasewrap':phasewrap,
        'phasesort':phasesort,
        'phasebin':phasebin,
        'minbinelems':minbinelems,
        'plotxlim':plotxlim,
        'lcfit':overplotfit,
    }

    # if we're returning stuff directly, i.e. not being used embedded within
    # the checkplot_dict function
    if directreturn or checkplotdict is None:

        return retdict

    # this requires the checkplotdict to be present already, we'll just update
    # it at the appropriate lspmethod and periodind
    else:

        if override_pfmethod:
            checkplotdict[override_pfmethod][periodind] = retdict
        else:
            checkplotdict[lspmethod][periodind] = retdict

        return checkplotdict