def make_fit_plot(phase, pmags, perrs, fitmags,
                  period, mintime, magseriesepoch,
                  plotfit,
                  magsarefluxes=False,
                  wrap=False,
                  model_over_lc=False):
    '''This makes a plot of the LC model fit.

    Parameters
    ----------

    phase,pmags,perrs : np.array
        The actual mag/flux time-series.

    fitmags : np.array
        The model fit time-series.

    period : float
        The period at which the phased LC was generated.

    mintime : float
        The minimum time value.

    magseriesepoch : float
        The value of time around which the phased LC was folded.

    plotfit : str
        The name of a file to write the plot to.

    magsarefluxes : bool
        Set this to True if the values in `pmags` and `fitmags` are actually
        fluxes.

    wrap : bool
        If True, will wrap the phased LC around 0.0 to make some phased LCs
        easier to look at.

    model_over_lc : bool
        Usually, this function will plot the actual LC over the model LC. Set
        this to True to plot the model over the actual LC; this is most useful
        when you have a very dense light curve and want to be able to see how it
        follows the model.

    Returns
    -------

    Nothing.

    '''

    # set up the figure
    plt.close('all')
    plt.figure(figsize=(8,4.8))

    if model_over_lc:
        model_z = 100
        lc_z = 0
    else:
        model_z = 0
        lc_z = 100


    if not wrap:

        plt.plot(phase, fitmags, linewidth=3.0, color='red',zorder=model_z)
        plt.plot(phase,pmags,
                 marker='o',
                 markersize=1.0,
                 linestyle='none',
                 rasterized=True, color='k',zorder=lc_z)

        # set the x axis ticks and label
        plt.gca().set_xticks(
            [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        )

    else:
        plt.plot(np.concatenate([phase-1.0,phase]),
                 np.concatenate([fitmags,fitmags]),
                 linewidth=3.0,
                 color='red',zorder=model_z)
        plt.plot(np.concatenate([phase-1.0,phase]),
                 np.concatenate([pmags,pmags]),
                 marker='o',
                 markersize=1.0,
                 linestyle='none',
                 rasterized=True, color='k',zorder=lc_z)

        plt.gca().set_xlim((-0.8,0.8))
        # set the x axis ticks and label
        plt.gca().set_xticks(
            [-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,
             0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
        )

    # set the y axis limit and label
    ymin, ymax = plt.ylim()
    if not magsarefluxes:
        plt.gca().invert_yaxis()
        plt.ylabel('magnitude')
    else:
        plt.ylabel('flux')


    plt.xlabel('phase')
    plt.title('period: %.6f, folded at %.6f, fit epoch: %.6f' %
              (period, mintime, magseriesepoch))
    plt.savefig(plotfit)
    plt.close()