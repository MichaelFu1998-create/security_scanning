def generate_rrab_lightcurve(
        times,
        mags=None,
        errs=None,
        paramdists={
            'period':sps.uniform(loc=0.45,scale=0.35),
            'fourierorder':[8,11],
            'amplitude':sps.uniform(loc=0.4,scale=0.5),
            'phioffset':np.pi,
        },
        magsarefluxes=False
):
    '''This generates fake RRab light curves.

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

            {'period', 'fourierorder', 'amplitude'}

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

            {'vartype': 'RRab',
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

    modeldict = generate_sinusoidal_lightcurve(times,
                                               mags=mags,
                                               errs=errs,
                                               paramdists=paramdists,
                                               magsarefluxes=magsarefluxes)
    modeldict['vartype'] = 'RRab'
    return modeldict