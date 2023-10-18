def _make_phased_magseries_plot(axes,
                                periodind,
                                stimes, smags, serrs,
                                varperiod, varepoch,
                                phasewrap, phasesort,
                                phasebin, minbinelems,
                                plotxlim,
                                lspmethod,
                                lspmethodind=0,
                                xliminsetmode=False,
                                twolspmode=False,
                                magsarefluxes=False,
                                verbose=True,
                                phasems=2.0,
                                phasebinms=4.0):
    '''Makes the phased magseries plot tile for the `checkplot_png` and
    `twolsp_checkplot_png` functions.

    Parameters
    ----------

    axes : matplotlib.axes.Axes object
        The Axes object where the generated plot will be written.

    periodind : int
        The index of the current best period being processed in the lspinfo
        dict.

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

    lspmethod : str
        One of the three-letter keys corresponding to period-finder method names
        in the `astrobase.plotbase.METHODSHORTLABELS` dict. Used to set the plot
        title correctly.

    lspmethodind : int
        If `twolspmode` is set, this will be used to look up the correct epoch
        associated with the current period-finder method and period.

    xliminsetmode : bool
        If this is True, the generated phased light curve plot will use the
        values of `plotxlim` as the main plot x-axis limits (i.e. zoomed-in if
        `plotxlim` is a range smaller than the full phase range), and will show
        the full phased light curve plot as an smaller inset. Useful for
        planetary transit light curves.

    twolspmode : bool
        If this is True, will use the `lspmethodind` and `periodind` to look up
        the correct values of epoch, etc. in the provided `varepoch` list of
        lists for plotting purposes.

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately.

    verbose : bool
        If True, indicates progress.

    phasems : float
        The marker size to use for the main phased light curve plot symbols.

    phasebinms : float
        The marker size to use for the binned phased light curve plot symbols.

    Returns
    -------

    Does not return anything, works on the input Axes object directly.

    '''

    plotvarepoch = None

    # figure out the epoch, if it's None, use the min of the time
    if varepoch is None:
        plotvarepoch = npmin(stimes)

    # if the varepoch is 'min', then fit a spline to the light curve
    # phased using the min of the time, find the fit mag minimum and use
    # the time for that as the varepoch
    elif isinstance(varepoch, str) and varepoch == 'min':

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
                plotvarepoch = varepoch[0]

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

    elif isinstance(varepoch, list):

        try:

            if twolspmode:

                thisvarepochlist = varepoch[lspmethodind]
                plotvarepoch = thisvarepochlist[periodind]

            else:
                plotvarepoch = varepoch[periodind]

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
        LOGINFO('plotting phased LC with period %.6f, epoch %.5f' %
                (varperiod, plotvarepoch))

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


    # finally, make the phased LC plot
    axes.plot(plotphase,
              plotmags,
              marker='o',
              ms=phasems, ls='None',mew=0,
              color='gray',
              rasterized=True)

    # overlay the binned phased LC plot if we're making one
    if phasebin:
        axes.plot(binplotphase,
                  binplotmags,
                  marker='o',
                  ms=phasebinms, ls='None',mew=0,
                  color='#1c1e57',
                  rasterized=True)

    # flip y axis for mags
    if not magsarefluxes:
        plot_ylim = axes.get_ylim()
        axes.set_ylim((plot_ylim[1], plot_ylim[0]))

    # set the x axis limit
    if not plotxlim:
        axes.set_xlim((npmin(plotphase)-0.1,
                       npmax(plotphase)+0.1))
    else:
        axes.set_xlim((plotxlim[0],plotxlim[1]))

    # make a grid
    axes.grid(color='#a9a9a9',
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

    axes.set_xlabel(plot_xlabel)
    axes.set_ylabel(plot_ylabel)

    # fix the yaxis ticks (turns off offset and uses the full
    # value of the yaxis tick)
    axes.get_yaxis().get_major_formatter().set_useOffset(False)
    axes.get_xaxis().get_major_formatter().set_useOffset(False)

    # make the plot title
    if periodind == 0:
        plottitle = '%s best period: %.6f d - epoch: %.5f' % (
            METHODSHORTLABELS[lspmethod],
            varperiod,
            plotvarepoch
        )
    elif periodind == 1 and not twolspmode:
        plottitle = '%s best period x 0.5: %.6f d - epoch: %.5f' % (
            METHODSHORTLABELS[lspmethod],
            varperiod,
            plotvarepoch
        )
    elif periodind == 2 and not twolspmode:
        plottitle = '%s best period x 2: %.6f d - epoch: %.5f' % (
            METHODSHORTLABELS[lspmethod],
            varperiod,
            plotvarepoch
        )
    elif periodind > 2 and not twolspmode:
        plottitle = '%s peak %s: %.6f d - epoch: %.5f' % (
            METHODSHORTLABELS[lspmethod],
            periodind-1,
            varperiod,
            plotvarepoch
        )
    elif periodind > 0:
        plottitle = '%s peak %s: %.6f d - epoch: %.5f' % (
            METHODSHORTLABELS[lspmethod],
            periodind+1,
            varperiod,
            plotvarepoch
        )

    axes.set_title(plottitle)

    # if we're making an inset plot showing the full range
    if (plotxlim and isinstance(plotxlim, (list,tuple)) and
        len(plotxlim) == 2 and xliminsetmode is True):

        # bump the ylim of the plot so that the inset can fit in this axes plot
        axesylim = axes.get_ylim()

        if magsarefluxes:
            axes.set_ylim(axesylim[0],
                          axesylim[1] + 0.5*npabs(axesylim[1]-axesylim[0]))
        else:
            axes.set_ylim(axesylim[0],
                          axesylim[1] - 0.5*npabs(axesylim[1]-axesylim[0]))

        # put the inset axes in
        inset = inset_axes(axes, width="40%", height="40%", loc=1)

        # make the scatter plot for the phased LC plot
        inset.plot(plotphase,
                   plotmags,
                   marker='o',
                   ms=2.0, ls='None',mew=0,
                   color='gray',
                   rasterized=True)

        # overlay the binned phased LC plot if we're making one
        if phasebin:
            inset.plot(binplotphase,
                       binplotmags,
                       marker='o',
                       ms=4.0, ls='None',mew=0,
                       color='#1c1e57',
                       rasterized=True)

        # show the full phase coverage
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
        inset.text(0.5,0.1,'full phased light curve',
                   ha='center',va='center',transform=inset.transAxes)
        # don't show axes labels or ticks
        inset.set_xticks([])
        inset.set_yticks([])