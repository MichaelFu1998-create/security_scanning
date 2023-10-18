def plot_phased_magseries(times,
                          mags,
                          period,
                          epoch='min',
                          fitknotfrac=0.01,
                          errs=None,
                          magsarefluxes=False,
                          normto='globalmedian',
                          normmingap=4.0,
                          sigclip=30.0,
                          phasewrap=True,
                          phasesort=True,
                          phasebin=None,
                          plotphaselim=(-0.8,0.8),
                          yrange=None,
                          xtimenotphase=False,
                          xaxlabel='phase',
                          yaxlabel=None,
                          modelmags=None,
                          modeltimes=None,
                          modelerrs=None,
                          outfile=None,
                          plotdpi=100):
    '''Plots a phased magnitude/flux time-series using the period provided.

    Parameters
    ----------

    times,mags : np.array
        The mag/flux time-series to plot as a function of phase given `period`.

    period : float
        The period to use to phase-fold the time-series. Should be the same unit
        as `times` (usually in days)

    epoch : 'min' or float or None
        This indicates how to get the epoch to use for phasing the light curve:

        - If None, uses the `min(times)` as the epoch for phasing.

        - If epoch is the string 'min', then fits a cubic spline to the phased
          light curve using `min(times)` as the initial epoch, finds the
          magnitude/flux minimum of this phased light curve fit, and finally
          uses the that time value as the epoch. This is useful for plotting
          planetary transits and eclipsing binary phased light curves so that
          phase 0.0 corresponds to the mid-center time of primary eclipse (or
          transit).

        - If epoch is a float, then uses that directly to phase the light
          curve and as the epoch of the phased mag series plot.

    fitknotfrac : float
        If `epoch='min'`, this function will attempt to fit a cubic spline to
        the phased light curve to find a time of light minimum as phase
        0.0. This kwarg sets the number of knots to generate the spline as a
        fraction of the total number of measurements in the input
        time-series. By default, this is set so that 100 knots are used to
        generate a spline for fitting the phased light curve consisting of 10000
        measurements.

    errs : np.array or None
        If this is provided, contains the measurement errors associated with
        each measurement of flux/mag in time-series. Providing this kwarg will
        add errbars to the output plot.

    magsarefluxes : bool
        Indicates if the input `mags` array is actually an array of flux
        measurements instead of magnitude measurements. If this is set to True,
        then the plot y-axis will be set as appropriate for mag or fluxes.

    normto : {'globalmedian', 'zero'} or a float
        Sets the normalization target::

          'globalmedian' -> norms each mag to the global median of the LC column
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

    plotphaselim : sequence of two floats or None
        The x-axis limits to use when making the phased light curve plot. By
        default, this is (-0.8, 0.8), which places phase 0.0 at the center of
        the plot and covers approximately two cycles in phase to make any trends
        clear.

    yrange : list of two floats or None
        This is used to provide a custom y-axis range to the plot. If None, will
        automatically determine y-axis range.

    xtimenotphase : bool
        If True, the x-axis gets units of time (multiplies phase by period).

    xaxlabel : str
        Sets the label for the x-axis.

    yaxlabel : str or None
        Sets the label for the y-axis. If this is None, the appropriate label
        will be used based on the value of the `magsarefluxes` kwarg.

    modeltimes,modelmags,modelerrs : np.array or None
        If all of these are provided, then this function will overplot the
        values of modeltimes and modelmags on top of the actual phased light
        curve. This is useful for plotting variability models on top of the
        light curve (e.g. plotting a Mandel-Agol transit model over the actual
        phased light curve. These arrays will be phased using the already
        provided period and epoch.

    outfile : str or StringIO/BytesIO or matplotlib.axes.Axes or None
        - a string filename for the file where the plot will be written.
        - a StringIO/BytesIO object to where the plot will be written.
        - a matplotlib.axes.Axes object to where the plot will be written.
        - if None, plots to 'magseries-phased-plot.png' in current dir.

    plotdpi : int
        Sets the resolution in DPI for PNG plots (default = 100).

    Returns
    -------

    str or StringIO/BytesIO or matplotlib.axes.Axes
        This returns based on the input:

        - If `outfile` is a str or None, the path to the generated plot file is
          returned.
        - If `outfile` is a StringIO/BytesIO object, will return the
          StringIO/BytesIO object to which the plot was written.
        - If `outfile` is a matplotlib.axes.Axes object, will return the Axes
          object with the plot elements added to it. One can then directly
          include this Axes object in some other Figure.

    '''

    # sigclip the magnitude timeseries
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # check if we need to normalize
    if normto is not False:
        stimes, smags = normalize_magseries(stimes, smags,
                                            normto=normto,
                                            magsarefluxes=magsarefluxes,
                                            mingap=normmingap)

        if ( isinstance(modelmags, np.ndarray) and
             isinstance(modeltimes, np.ndarray) ):

            stimes, smags = normalize_magseries(modeltimes, modelmags,
                                                normto=normto,
                                                magsarefluxes=magsarefluxes,
                                                mingap=normmingap)

    # figure out the epoch, if it's None, use the min of the time
    if epoch is None:
        epoch = stimes.min()

    # if the epoch is 'min', then fit a spline to the light curve phased
    # using the min of the time, find the fit mag minimum and use the time for
    # that as the epoch
    elif isinstance(epoch, str) and epoch == 'min':

        try:
            spfit = spline_fit_magseries(stimes, smags, serrs, period,
                                         knotfraction=fitknotfrac)
            epoch = spfit['fitinfo']['fitepoch']
            if len(epoch) != 1:
                epoch = epoch[0]
        except Exception as e:
            LOGEXCEPTION('spline fit failed, using min(times) as epoch')
            epoch = npmin(stimes)


    # now phase the data light curve (and optionally, phase bin the light curve)
    if errs is not None:

        phasedlc = phase_magseries_with_errs(stimes, smags, serrs, period,
                                             epoch, wrap=phasewrap,
                                             sort=phasesort)
        plotphase = phasedlc['phase']
        plotmags = phasedlc['mags']
        ploterrs = phasedlc['errs']

        # if we're supposed to bin the phases, do so
        if phasebin:

            binphasedlc = phase_bin_magseries_with_errs(plotphase, plotmags,
                                                        ploterrs,
                                                        binsize=phasebin)
            binplotphase = binphasedlc['binnedphases']
            binplotmags = binphasedlc['binnedmags']
            binploterrs = binphasedlc['binnederrs']

    else:

        phasedlc = phase_magseries(stimes, smags, period, epoch,
                                   wrap=phasewrap, sort=phasesort)
        plotphase = phasedlc['phase']
        plotmags = phasedlc['mags']
        ploterrs = None

        # if we're supposed to bin the phases, do so
        if phasebin:

            binphasedlc = phase_bin_magseries(plotphase,
                                              plotmags,
                                              binsize=phasebin)
            binplotphase = binphasedlc['binnedphases']
            binplotmags = binphasedlc['binnedmags']
            binploterrs = None

    # phase the model light curve
    modelplotphase, modelplotmags = None, None

    if ( isinstance(modelerrs,np.ndarray) and
         isinstance(modeltimes,np.ndarray) and
         isinstance(modelmags,np.ndarray) ):

        modelphasedlc = phase_magseries_with_errs(modeltimes, modelmags,
                                                  modelerrs, period, epoch,
                                                  wrap=phasewrap,
                                                  sort=phasesort)
        modelplotphase = modelphasedlc['phase']
        modelplotmags = modelphasedlc['mags']

    # note that we never will phase-bin the model (no point).
    elif ( not isinstance(modelerrs,np.ndarray) and
           isinstance(modeltimes,np.ndarray) and
           isinstance(modelmags,np.ndarray) ):

        modelphasedlc = phase_magseries(modeltimes, modelmags, period, epoch,
                                        wrap=phasewrap, sort=phasesort)
        modelplotphase = modelphasedlc['phase']
        modelplotmags = modelphasedlc['mags']

    # finally, make the plots

    # check if the outfile is actually an Axes object
    if isinstance(outfile, matplotlib.axes.Axes):
        ax = outfile

    # otherwise, it's just a normal file or StringIO/BytesIO
    else:
        fig = plt.figure()
        fig.set_size_inches(7.5,4.8)
        ax = plt.gca()

    if xtimenotphase:
        plotphase *= period

    if phasebin:
        ax.errorbar(plotphase, plotmags, fmt='o',
                    color='#B2BEB5',
                    yerr=ploterrs,
                    markersize=3.0,
                    markeredgewidth=0.0,
                    ecolor='#B2BEB5',
                    capsize=0)
        if xtimenotphase:
            binplotphase *= period
        ax.errorbar(binplotphase, binplotmags, fmt='bo', yerr=binploterrs,
                    markersize=5.0, markeredgewidth=0.0, ecolor='#B2BEB5',
                    capsize=0)

    else:
        ax.errorbar(plotphase, plotmags, fmt='ko', yerr=ploterrs,
                    markersize=3.0, markeredgewidth=0.0, ecolor='#B2BEB5',
                    capsize=0)

    if (isinstance(modelplotphase, np.ndarray) and
        isinstance(modelplotmags, np.ndarray)):

        if xtimenotphase:
            modelplotphase *= period
        ax.plot(modelplotphase, modelplotmags, zorder=5, linewidth=2,
                alpha=0.9, color='#181c19')

    # make a grid
    ax.grid(color='#a9a9a9',
            alpha=0.9,
            zorder=0,
            linewidth=1.0,
            linestyle=':')

    # make lines for phase 0.0, 0.5, and -0.5
    ax.axvline(0.0,alpha=0.9,linestyle='dashed',color='g')
    if not xtimenotphase:
        ax.axvline(-0.5,alpha=0.9,linestyle='dashed',color='g')
        ax.axvline(0.5,alpha=0.9,linestyle='dashed',color='g')
    else:
        ax.axvline(-period*0.5,alpha=0.9,linestyle='dashed',color='g')
        ax.axvline(period*0.5,alpha=0.9,linestyle='dashed',color='g')

    # fix the ticks to use no offsets
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)

    # get the yrange
    if yrange and isinstance(yrange,(list,tuple)) and len(yrange) == 2:
        ymin, ymax = yrange
    else:
        ymin, ymax = ax.get_ylim()

    # set the y axis labels and range
    if not yaxlabel:
        if not magsarefluxes:
            ax.set_ylim(ymax, ymin)
            yaxlabel = 'magnitude'
        else:
            ax.set_ylim(ymin, ymax)
            yaxlabel = 'flux'

    # set the x axis limit
    if not plotphaselim:
        ax.set_xlim((npmin(plotphase)-0.1,
                     npmax(plotphase)+0.1))
    else:
        if xtimenotphase:
            ax.set_xlim((period*plotphaselim[0],period*plotphaselim[1]))
        else:
            ax.set_xlim((plotphaselim[0],plotphaselim[1]))

    # set up the axis labels and plot title
    ax.set_xlabel(xaxlabel)
    ax.set_ylabel(yaxlabel)
    ax.set_title('period: %.6f d - epoch: %.6f' % (period, epoch))

    LOGINFO('using period: %.6f d and epoch: %.6f' % (period, epoch))

    # check if the output filename is actually an instance of StringIO
    if sys.version_info[:2] < (3,0):

        is_Strio = isinstance(outfile, cStringIO.InputType)

    else:

        is_Strio = isinstance(outfile, Strio)

    # make the figure
    if (outfile and
        not is_Strio and
        not isinstance(outfile, matplotlib.axes.Axes)):

        if outfile.endswith('.png'):
            fig.savefig(outfile, bbox_inches='tight', dpi=plotdpi)
        else:
            fig.savefig(outfile, bbox_inches='tight')
        plt.close()
        return period, epoch, os.path.abspath(outfile)

    elif outfile and is_Strio:

        fig.savefig(outfile, bbox_inches='tight', dpi=plotdpi, format='png')
        return outfile

    elif outfile and isinstance(outfile, matplotlib.axes.Axes):

        return outfile

    elif not outfile and dispok:

        plt.show()
        plt.close()
        return period, epoch

    else:

        LOGWARNING('no output file specified and no $DISPLAY set, '
                   'saving to magseries-phased-plot.png in current directory')
        outfile = 'magseries-phased-plot.png'
        plt.savefig(outfile, bbox_inches='tight', dpi=plotdpi)
        plt.close()
        return period, epoch, os.path.abspath(outfile)