def generate_flare_lightcurve(
        times,
        mags=None,
        errs=None,
        paramdists={
            # flare peak amplitude from 0.01 mag to 1.0 mag above median.  this
            # is tuned for redder bands, flares are much stronger in bluer
            # bands, so tune appropriately for your situation.
            'amplitude':sps.uniform(loc=0.01,scale=0.99),
            # up to 5 flares per LC and at least 1
            'nflares':[1,5],
            # 10 minutes to 1 hour for rise stdev
            'risestdev':sps.uniform(loc=0.007, scale=0.04),
            # 1 hour to 4 hours for decay time constant
            'decayconst':sps.uniform(loc=0.04, scale=0.163)
        },
        magsarefluxes=False,
):
    '''This generates fake flare light curves.

    Parameters
    ----------

    times : np.array
        This is an array of time values that will be used as the time base.

    mags,errs : np.array
        These arrays will have the model added to them. If either is
        None, `np.full_like(times, 0.0)` will used as a substitute and the model
        light curve will be centered around 0.0.

    paramdists : dict
        This is a dict containing parameter distributions to use for the
        model params, containing the following keys ::

            {'amplitude', 'nflares', 'risestdev', 'decayconst'}

        The values of these keys should all be 'frozen' scipy.stats distribution
        objects, e.g.:

        https://docs.scipy.org/doc/scipy/reference/stats.html#continuous-distributions
        The `flare_peak_time` for each flare will be generated automatically
        between `times.min()` and `times.max()` using a uniform distribution.

        The `amplitude` will be flipped automatically as appropriate if
        `magsarefluxes=True`.

    magsarefluxes : bool
        If the generated time series is meant to be a flux time-series, set this
        to True to get the correct sign of variability amplitude.

    Returns
    -------

    dict
        A dict of the form below is returned::

            {'vartype': 'flare',
             'params': {'amplitude': generated value of flare amplitudes,
                        'nflares': generated value of number of flares,
                        'risestdev': generated value of stdev of rise time,
                        'decayconst': generated value of decay constant,
                        'peaktime': generated value of flare peak time},
             'times': the model times,
             'mags': the model mags,
             'errs': the model errs,
             'varamplitude': the generated amplitude of
                             variability == 'amplitude'}

    '''

    if mags is None:
        mags = np.full_like(times, 0.0)

    if errs is None:
        errs = np.full_like(times, 0.0)

    nflares = npr.randint(paramdists['nflares'][0],
                          high=paramdists['nflares'][1])

    # generate random flare peak times based on the number of flares
    flarepeaktimes = (
        npr.random(
            size=nflares
        )*(times.max() - times.min()) + times.min()
    )

    # now add the flares to the time-series
    params = {'nflares':nflares}

    for flareind, peaktime in zip(range(nflares), flarepeaktimes):

        # choose the amplitude, rise stdev and decay time constant
        amp = paramdists['amplitude'].rvs(size=1)
        risestdev = paramdists['risestdev'].rvs(size=1)
        decayconst = paramdists['decayconst'].rvs(size=1)

        # fix the transit depth if it needs to be flipped
        if magsarefluxes and amp < 0.0:
            amp = -amp
        elif not magsarefluxes and amp > 0.0:
            amp = -amp

        # add this flare to the light curve
        modelmags, ptimes, pmags, perrs = (
            flares.flare_model(
                [amp, peaktime, risestdev, decayconst],
                times,
                mags,
                errs
            )
        )

        # update the mags
        mags = modelmags

        # add the flare params to the modeldict
        params[flareind] = {'peaktime':peaktime,
                            'amplitude':amp,
                            'risestdev':risestdev,
                            'decayconst':decayconst}


    #
    # done with all flares
    #

    # return a dict with everything
    modeldict = {
        'vartype':'flare',
        'params':params,
        'times':times,
        'mags':mags,
        'errs':errs,
        'varperiod':None,
        # FIXME: this is complicated because we can have multiple flares
        # figure out a good way to handle this upstream
        'varamplitude':[params[x]['amplitude']
                        for x in range(params['nflares'])],
    }

    return modeldict