def _pkl_magseries_plot(stimes, smags, serrs,
                        plotdpi=100,
                        magsarefluxes=False):
    '''This returns the magseries plot PNG as base64, plus arrays as dict.

    Parameters
    ----------

    stimes,smags,serrs : np.array
        The mag/flux time-series arrays along with associated errors. These
        should all have been run through nan-stripping and sigma-clipping
        beforehand.

    plotdpi : int
        The resolution of the plot to make in DPI.

    magsarefluxes : bool
        If True, indicates the input time-series is fluxes and not mags so the
        plot y-axis direction and range can be set appropriately.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'magseries': {'plot': base64 encoded str representation of the
                                   magnitude/flux time-series plot,
                           'times': the `stimes` array,
                           'mags': the `smags` array,
                           'errs': the 'serrs' array}}

        The dict is returned in this format so it can be directly incorporated
        in a checkplotdict, using Python's dict `update()` method.

    '''

    scaledplottime = stimes - npmin(stimes)

    # open the figure instance
    magseriesfig = plt.figure(figsize=(7.5,4.8),dpi=plotdpi)

    plt.plot(scaledplottime,
             smags,
             marker='o',
             ms=2.0, ls='None',mew=0,
             color='green',
             rasterized=True)

    # flip y axis for mags
    if not magsarefluxes:
        plot_ylim = plt.ylim()
        plt.ylim((plot_ylim[1], plot_ylim[0]))

    # set the x axis limit
    plt.xlim((npmin(scaledplottime)-2.0,
              npmax(scaledplottime)+2.0))

    # make a grid
    plt.grid(color='#a9a9a9',
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

    plt.xlabel(plot_xlabel)
    plt.ylabel(plot_ylabel)

    # fix the yaxis ticks (turns off offset and uses the full
    # value of the yaxis tick)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

    # this is the output instance
    magseriespng = StrIO()
    magseriesfig.savefig(magseriespng,
                         # bbox_inches='tight',
                         pad_inches=0.05, format='png')
    plt.close()

    # encode the finderpng instance to base64
    magseriespng.seek(0)
    magseriesb64 = base64.b64encode(magseriespng.read())

    # close the stringio buffer
    magseriespng.close()

    checkplotdict = {
        'magseries':{
            'plot':magseriesb64,
            'times':stimes,
            'mags':smags,
            'errs':serrs
        }
    }

    return checkplotdict