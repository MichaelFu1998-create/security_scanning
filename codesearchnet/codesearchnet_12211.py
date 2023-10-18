def plot_magseries(times,
                   mags,
                   magsarefluxes=False,
                   errs=None,
                   out=None,
                   sigclip=30.0,
                   normto='globalmedian',
                   normmingap=4.0,
                   timebin=None,
                   yrange=None,
                   segmentmingap=100.0,
                   plotdpi=100):
    '''This plots a magnitude/flux time-series.

    Parameters
    ----------

    times,mags : np.array
        The mag/flux time-series to plot as a function of time.

    magsarefluxes : bool
        Indicates if the input `mags` array is actually an array of flux
        measurements instead of magnitude measurements. If this is set to True,
        then the plot y-axis will be set as appropriate for mag or fluxes. In
        addition:

        - if `normto` is 'zero', then the median flux is divided from each
          observation's flux value to yield normalized fluxes with 1.0 as the
          global median.
        - if `normto` is 'globalmedian', then the global median flux value
          across the entire time series is multiplied with each measurement.
        - if `norm` is set to a `float`, then this number is multiplied with the
          flux value for each measurement.

    errs : np.array or None
        If this is provided, contains the measurement errors associated with
        each measurement of flux/mag in time-series. Providing this kwarg will
        add errbars to the output plot.

    out : str or StringIO/BytesIO object or None
        Sets the output type and target:

        - If `out` is a string, will save the plot to the specified file name.
        - If `out` is a StringIO/BytesIO object, will save the plot to that file
          handle. This can be useful to carry out additional operations on the
          output binary stream, or convert it to base64 text for embedding in
          HTML pages.
        - If `out` is None, will save the plot to a file called
          'magseries-plot.png' in the current working directory.

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

    normto : {'globalmedian', 'zero'} or a float
        Sets the normalization target::

          'globalmedian' -> norms each mag to the global median of the LC column
          'zero'         -> norms each mag to zero
          a float        -> norms each mag to this specified float value.

    normmingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    timebin : float or None
        The bin size to use to group together measurements closer than this
        amount in time. This is in seconds. If this is None, no time-binning
        will be performed.

    yrange : list of two floats or None
        This is used to provide a custom y-axis range to the plot. If None, will
        automatically determine y-axis range.

    segmentmingap : float or None
        This controls the minimum length of time (in days) required to consider
        a timegroup in the light curve as a separate segment. This is useful
        when the light curve consists of measurements taken over several
        seasons, so there's lots of dead space in the plot that can be cut out
        to zoom in on the interesting stuff. If `segmentmingap` is not None, the
        magseries plot will be cut in this way and the x-axis will show these
        breaks.

    plotdpi : int
        Sets the resolution in DPI for PNG plots (default = 100).

    Returns
    -------

    str or BytesIO/StringIO object
        Returns based on the input:

        - If `out` is a str or None, the path to the generated plot file is
          returned.
        - If `out` is a StringIO/BytesIO object, will return the
          StringIO/BytesIO object to which the plot was written.

    '''

    # sigclip the magnitude timeseries
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # now we proceed to binning
    if timebin and errs is not None:

        binned = time_bin_magseries_with_errs(stimes, smags, serrs,
                                              binsize=timebin)
        btimes, bmags, berrs = (binned['binnedtimes'],
                                binned['binnedmags'],
                                binned['binnederrs'])

    elif timebin and errs is None:

        binned = time_bin_magseries(stimes, smags,
                                    binsize=timebin)
        btimes, bmags, berrs = binned['binnedtimes'], binned['binnedmags'], None

    else:

        btimes, bmags, berrs = stimes, smags, serrs


    # check if we need to normalize
    if normto is not False:
        btimes, bmags = normalize_magseries(btimes, bmags,
                                            normto=normto,
                                            magsarefluxes=magsarefluxes,
                                            mingap=normmingap)

    btimeorigin = btimes.min()
    btimes = btimes - btimeorigin

    ##################################
    ## FINALLY PLOT THE LIGHT CURVE ##
    ##################################

    # if we're going to plot with segment gaps highlighted, then find the gaps
    if segmentmingap is not None:
        ntimegroups, timegroups = find_lc_timegroups(btimes,
                                                     mingap=segmentmingap)

    # get the yrange for all the plots if it's given
    if yrange and isinstance(yrange,(list,tuple)) and len(yrange) == 2:
        ymin, ymax = yrange

    # if it's not given, figure it out
    else:

        # the plot y limits are just 0.05 mags on each side if mags are used
        if not magsarefluxes:
            ymin, ymax = (bmags.min() - 0.05,
                          bmags.max() + 0.05)
        # if we're dealing with fluxes, limits are 2% of the flux range per side
        else:
            ycov = bmags.max() - bmags.min()
            ymin = bmags.min() - 0.02*ycov
            ymax = bmags.max() + 0.02*ycov

    # if we're supposed to make the plot segment-aware (i.e. gaps longer than
    # segmentmingap will be cut out)
    if segmentmingap and ntimegroups > 1:

        LOGINFO('%s time groups found' % ntimegroups)

        # our figure is now a multiple axis plot
        # the aspect ratio is a bit wider
        fig, axes = plt.subplots(1,ntimegroups,sharey=True)
        fig.set_size_inches(10,4.8)
        axes = np.ravel(axes)

        # now go through each axis and make the plots for each timegroup
        for timegroup, ax, axind in zip(timegroups, axes, range(len(axes))):

            tgtimes = btimes[timegroup]
            tgmags = bmags[timegroup]

            if berrs:
                tgerrs = berrs[timegroup]
            else:
                tgerrs = None

            LOGINFO('axes: %s, timegroup %s: JD %.3f to %.3f' % (
                axind,
                axind+1,
                btimeorigin + tgtimes.min(),
                btimeorigin + tgtimes.max())
            )

            ax.errorbar(tgtimes, tgmags, fmt='go', yerr=tgerrs,
                        markersize=2.0, markeredgewidth=0.0, ecolor='grey',
                        capsize=0)

            # don't use offsets on any xaxis
            ax.get_xaxis().get_major_formatter().set_useOffset(False)

            # fix the ticks to use no yoffsets and remove right spines for first
            # axes instance
            if axind == 0:
                ax.get_yaxis().get_major_formatter().set_useOffset(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.tick_left()
            # remove the right and left spines for the other axes instances
            elif 0 < axind < (len(axes)-1):
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.tick_params(right='off', labelright='off',
                               left='off',labelleft='off')
            # make the left spines invisible for the last axes instance
            elif axind == (len(axes)-1):
                ax.spines['left'].set_visible(False)
                ax.spines['right'].set_visible(True)
                ax.yaxis.tick_right()

            # set the yaxis limits
            if not magsarefluxes:
                ax.set_ylim(ymax, ymin)
            else:
                ax.set_ylim(ymin, ymax)

            # now figure out the xaxis ticklabels and ranges
            tgrange = tgtimes.max() - tgtimes.min()

            if tgrange < 10.0:
                ticklocations = [tgrange/2.0]
                ax.set_xlim(npmin(tgtimes) - 0.5, npmax(tgtimes) + 0.5)
            elif 10.0 < tgrange < 30.0:
                ticklocations = np.linspace(tgtimes.min()+5.0,
                                            tgtimes.max()-5.0,
                                            num=2)
                ax.set_xlim(npmin(tgtimes) - 2.0, npmax(tgtimes) + 2.0)

            elif 30.0 < tgrange < 100.0:
                ticklocations = np.linspace(tgtimes.min()+10.0,
                                            tgtimes.max()-10.0,
                                            num=3)
                ax.set_xlim(npmin(tgtimes) - 2.5, npmax(tgtimes) + 2.5)
            else:
                ticklocations = np.linspace(tgtimes.min()+20.0,
                                            tgtimes.max()-20.0,
                                            num=3)
                ax.set_xlim(npmin(tgtimes) - 3.0, npmax(tgtimes) + 3.0)

            ax.xaxis.set_ticks([int(x) for x in ticklocations])

        # done with plotting all the sub axes

        # make the distance between sub plots smaller
        plt.subplots_adjust(wspace=0.07)

        # make the overall x and y labels
        fig.text(0.5, 0.00, 'JD - %.3f (not showing gaps > %.2f d)' %
                 (btimeorigin, segmentmingap), ha='center')
        if not magsarefluxes:
            fig.text(0.02, 0.5, 'magnitude', va='center', rotation='vertical')
        else:
            fig.text(0.02, 0.5, 'flux', va='center', rotation='vertical')


    # make normal figure otherwise
    else:

        fig = plt.figure()
        fig.set_size_inches(7.5,4.8)

        plt.errorbar(btimes, bmags, fmt='go', yerr=berrs,
                     markersize=2.0, markeredgewidth=0.0, ecolor='grey',
                     capsize=0)

        # make a grid
        plt.grid(color='#a9a9a9',
                 alpha=0.9,
                 zorder=0,
                 linewidth=1.0,
                 linestyle=':')

        # fix the ticks to use no offsets
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

        plt.xlabel('JD - %.3f' % btimeorigin)

        # set the yaxis limits and labels
        if not magsarefluxes:
            plt.ylim(ymax, ymin)
            plt.ylabel('magnitude')
        else:
            plt.ylim(ymin, ymax)
            plt.ylabel('flux')

    # check if the output filename is actually an instance of StringIO
    if sys.version_info[:2] < (3,0):

        is_Strio = isinstance(out, cStringIO.InputType)

    else:

        is_Strio = isinstance(out, Strio)


    # write the plot out to a file if requested
    if out and not is_Strio:

        if out.endswith('.png'):
            plt.savefig(out,bbox_inches='tight',dpi=plotdpi)
        else:
            plt.savefig(out,bbox_inches='tight')
        plt.close()
        return os.path.abspath(out)

    elif out and is_Strio:

        plt.savefig(out, bbox_inches='tight', dpi=plotdpi, format='png')
        return out

    elif not out and dispok:

        plt.show()
        plt.close()
        return

    else:

        LOGWARNING('no output file specified and no $DISPLAY set, '
                   'saving to magseries-plot.png in current directory')
        outfile = 'magseries-plot.png'
        plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
        plt.close()
        return os.path.abspath(outfile)