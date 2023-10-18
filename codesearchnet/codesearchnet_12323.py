def _make_magseries_plot(axes,
                         stimes,
                         smags,
                         serrs,
                         magsarefluxes=False,
                         ms=2.0):
    '''Makes the mag-series plot tile for `checkplot_png` and
    `twolsp_checkplot_png`.

    axes : matplotlib.axes.Axes object
        The Axes object where the generated plot will go.

    stimes,smags,serrs : np.array
        The mag/flux time-series arrays along with associated errors. These
        should all have been run through nan-stripping and sigma-clipping
        beforehand.

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately.

    ms : float
        The `markersize` kwarg to use when making the mag-series plot.

    Returns
    -------

    Does not return anything, works on the input Axes object directly.

    '''

    scaledplottime = stimes - npmin(stimes)

    axes.plot(scaledplottime,
              smags,
              marker='o',
              ms=ms, ls='None',mew=0,
              color='green',
              rasterized=True)

    # flip y axis for mags
    if not magsarefluxes:
        plot_ylim = axes.get_ylim()
        axes.set_ylim((plot_ylim[1], plot_ylim[0]))

    # set the x axis limit
    axes.set_xlim((npmin(scaledplottime)-1.0,
                   npmax(scaledplottime)+1.0))

    # make a grid
    axes.grid(color='#a9a9a9',
              alpha=0.9,
              zorder=0,
              linewidth=1.0,
              linestyle=':')

    # make the x and y axis labels
    plot_xlabel = 'JD - %.3f' % npmin(stimes)
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