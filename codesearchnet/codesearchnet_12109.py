def get_frequency_grid(times,
                       samplesperpeak=5,
                       nyquistfactor=5,
                       minfreq=None,
                       maxfreq=None,
                       returnf0dfnf=False):
    '''This calculates a frequency grid for the period finding functions in this
    module.

    Based on the autofrequency function in astropy.stats.lombscargle.

    http://docs.astropy.org/en/stable/_modules/astropy/stats/lombscargle/core.html#LombScargle.autofrequency

    Parameters
    ----------

    times : np.array
        The times to use to generate the frequency grid over.

    samplesperpeak : int
        The minimum sample coverage each frequency point in the grid will get.

    nyquistfactor : int
        The multiplier over the Nyquist rate to use.

    minfreq,maxfreq : float or None
        If not None, these will be the limits of the frequency grid generated.

    returnf0dfnf : bool
        If this is True, will return the values of `f0`, `df`, and `Nf`
        generated for this grid.

    Returns
    -------

    np.array
        A grid of frequencies.

    '''

    baseline = times.max() - times.min()
    nsamples = times.size

    df = 1. / baseline / samplesperpeak

    if minfreq is not None:
        f0 = minfreq
    else:
        f0 = 0.5 * df

    if maxfreq is not None:
        Nf = int(np.ceil((maxfreq - f0) / df))
    else:
        Nf = int(0.5 * samplesperpeak * nyquistfactor * nsamples)


    if returnf0dfnf:
        return f0, df, Nf, f0 + df * np.arange(Nf)
    else:
        return f0 + df * np.arange(Nf)