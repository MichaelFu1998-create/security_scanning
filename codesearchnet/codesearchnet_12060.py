def plot_acf_results(acfp, outfile, maxlags=5000, yrange=(-0.4,0.4)):
    '''
    This plots the unsmoothed/smoothed ACF vs lag.

    Parameters
    ----------

    acfp : dict
        This is the dict returned from `macf_period_find` below.

    outfile : str
        The output file the plot will be written to.

    maxlags: int
        The maximum number of lags to include in the plot.

    yrange : sequence of two floats
        The y-range of the ACF vs. lag plot to use.

    '''

    import matplotlib.pyplot as plt

    lags = acfp['acfresults']['lags'][:maxlags]
    smoothedacf = acfp['acf'][:maxlags]
    unsmoothedacf = acfp['acfresults']['acf'][:maxlags]

    acfparams = acfp['kwargs']['smoothfunckwargs'].copy()
    acfparams.update({'peakinterval': int(acfp['kwargs']['smoothacf']/2.0)})

    # plot the ACFs
    fig, ax1 = plt.subplots()

    # this is lags vs acf
    ax1.plot(lags, unsmoothedacf, label='unsmoothed ACF',color='#1f77b4')
    ax1.plot(lags, smoothedacf, label='smoothed ACF', color='#ff7f0e')

    ax1.set_xlim((0,maxlags))

    ax1.set_xlabel('lags')

    # overplot the identified peaks
    acfmaxinds = acfp['acfpeaks']['maxinds']

    for i, maxind in enumerate(acfmaxinds):
        if i == 0:
            ax1.axvline(maxind,
                        linewidth=2.0,
                        color='red',
                        ymin=0.2, ymax=0.3,
                        label='identified ACF peaks')
        else:
            ax1.axvline(maxind,
                        linewidth=2.0,
                        color='red',
                        ymin=0.2, ymax=0.3)

    plt.ylabel('ACF')
    plt.ylim(yrange)
    ax1.legend()
    plt.title('%s' % repr(acfparams))
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close('all')

    return outfile