def generate_sinusoidal_lightcurve(
        times,
        mags=None,
        errs=None,
        paramdists={
            'period':sps.uniform(loc=0.04,scale=500.0),
            'fourierorder':[2,10],
            'amplitude':sps.uniform(loc=0.1,scale=0.9),
            'phioffset':0.0,
        },
        magsarefluxes=False
):
    '''This generates fake sinusoidal light curves.

    This can be used for a variety of sinusoidal variables, e.g. RRab, RRc,
    Cepheids, Miras, etc. The functions that generate these model LCs below
    implement the following table::

        ## FOURIER PARAMS FOR SINUSOIDAL VARIABLES
        #
        # type        fourier           period [days]
        #             order    dist     limits         dist

        # RRab        8 to 10  uniform  0.45--0.80     uniform
        # RRc         3 to 6   uniform  0.10--0.40     uniform
        # HADS        7 to 9   uniform  0.04--0.10     uniform
        # rotator     2 to 5   uniform  0.80--120.0    uniform
        # LPV         2 to 5   uniform  250--500.0     uniform

    FIXME: for better model LCs, figure out how scipy.signal.butter works and
    low-pass filter using scipy.signal.filtfilt.

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

            {'period', 'fourierorder', 'amplitude', 'phioffset'}

        The values of these keys should all be 'frozen' scipy.stats distribution
        objects, e.g.:

        https://docs.scipy.org/doc/scipy/reference/stats.html#continuous-distributions
        The variability epoch will be automatically chosen from a uniform
        distribution between `times.min()` and `times.max()`.

        The `amplitude` will be flipped automatically as appropriate if
        `magsarefluxes=True`.

    magsarefluxes : bool
        If the generated time series is meant to be a flux time-series, set this
        to True to get the correct sign of variability amplitude.

    Returns
    -------

    dict
        A dict of the form below is returned::

            {'vartype': 'sinusoidal',
             'params': {'period': generated value of period,
                        'epoch': generated value of epoch,
                        'amplitude': generated value of amplitude,
                        'fourierorder': generated value of fourier order,
                        'fourieramps': generated values of fourier amplitudes,
                        'fourierphases': generated values of fourier phases},
             'times': the model times,
             'mags': the model mags,
             'errs': the model errs,
             'varperiod': the generated period of variability == 'period'
             'varamplitude': the generated amplitude of
                             variability == 'amplitude'}

    '''

    if mags is None:
        mags = np.full_like(times, 0.0)

    if errs is None:
        errs = np.full_like(times, 0.0)

    # choose the epoch
    epoch = npr.random()*(times.max() - times.min()) + times.min()

    # choose the period, fourierorder, and amplitude
    period = paramdists['period'].rvs(size=1)
    fourierorder = npr.randint(paramdists['fourierorder'][0],
                               high=paramdists['fourierorder'][1])
    amplitude = paramdists['amplitude'].rvs(size=1)

    # fix the amplitude if it needs to be flipped
    if magsarefluxes and amplitude < 0.0:
        amplitude = -amplitude
    elif not magsarefluxes and amplitude > 0.0:
        amplitude = -amplitude

    # generate the amplitudes and phases of the Fourier components
    ampcomps = [abs(amplitude/2.0)/float(x)
                for x in range(1,fourierorder+1)]
    phacomps = [paramdists['phioffset']*float(x)
                for x in range(1,fourierorder+1)]

    # now that we have our amp and pha components, generate the light curve
    modelmags, phase, ptimes, pmags, perrs = sinusoidal.sine_series_sum(
        [period, epoch, ampcomps, phacomps],
        times,
        mags,
        errs
    )

    # resort in original time order
    timeind = np.argsort(ptimes)
    mtimes = ptimes[timeind]
    mmags = modelmags[timeind]
    merrs = perrs[timeind]
    mphase = phase[timeind]

    # return a dict with everything
    modeldict = {
        'vartype':'sinusoidal',
        'params':{x:y for x,y in zip(['period',
                                      'epoch',
                                      'amplitude',
                                      'fourierorder',
                                      'fourieramps',
                                      'fourierphases'],
                                     [period,
                                      epoch,
                                      amplitude,
                                      fourierorder,
                                      ampcomps,
                                      phacomps])},
        'times':mtimes,
        'mags':mmags,
        'errs':merrs,
        'phase':mphase,
        # these are standard keys that help with later characterization of
        # variability as a function period, variability amplitude, object mag,
        # ndet, etc.
        'varperiod':period,
        'varamplitude':amplitude
    }

    return modeldict