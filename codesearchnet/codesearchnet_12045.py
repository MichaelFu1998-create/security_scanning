def generate_transit_lightcurve(
        times,
        mags=None,
        errs=None,
        paramdists={'transitperiod':sps.uniform(loc=0.1,scale=49.9),
                    'transitdepth':sps.uniform(loc=1.0e-4,scale=2.0e-2),
                    'transitduration':sps.uniform(loc=0.01,scale=0.29)},
        magsarefluxes=False,
):
    '''This generates fake planet transit light curves.

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

            {'transitperiod', 'transitdepth', 'transitduration'}

        The values of these keys should all be 'frozen' scipy.stats distribution
        objects, e.g.:

        https://docs.scipy.org/doc/scipy/reference/stats.html#continuous-distributions
        The variability epoch will be automatically chosen from a uniform
        distribution between `times.min()` and `times.max()`.

        The ingress duration will be automatically chosen from a uniform
        distribution ranging from 0.05 to 0.5 of the transitduration.

        The transitdepth will be flipped automatically as appropriate if
        `magsarefluxes=True`.

    magsarefluxes : bool
        If the generated time series is meant to be a flux time-series, set this
        to True to get the correct sign of variability amplitude.

    Returns
    -------

    dict
        A dict of the form below is returned::

            {'vartype': 'planet',
             'params': {'transitperiod': generated value of period,
                        'transitepoch': generated value of epoch,
                        'transitdepth': generated value of transit depth,
                        'transitduration': generated value of transit duration,
                        'ingressduration': generated value of transit ingress
                                           duration},
             'times': the model times,
             'mags': the model mags,
             'errs': the model errs,
             'varperiod': the generated period of variability == 'transitperiod'
             'varamplitude': the generated amplitude of
                             variability == 'transitdepth'}

    '''

    if mags is None:
        mags = np.full_like(times, 0.0)

    if errs is None:
        errs = np.full_like(times, 0.0)

    # choose the epoch
    epoch = npr.random()*(times.max() - times.min()) + times.min()

    # choose the period, depth, duration
    period = paramdists['transitperiod'].rvs(size=1)
    depth = paramdists['transitdepth'].rvs(size=1)
    duration = paramdists['transitduration'].rvs(size=1)

    # figure out the ingress duration
    ingduration = npr.random()*(0.5*duration - 0.05*duration) + 0.05*duration

    # fix the transit depth if it needs to be flipped
    if magsarefluxes and depth < 0.0:
        depth = -depth
    elif not magsarefluxes and depth > 0.0:
        depth = -depth

    # generate the model
    modelmags, phase, ptimes, pmags, perrs = (
        transits.trapezoid_transit_func([period, epoch, depth,
                                         duration, ingduration],
                                        times,
                                        mags,
                                        errs)
    )

    # resort in original time order
    timeind = np.argsort(ptimes)
    mtimes = ptimes[timeind]
    mmags = modelmags[timeind]
    merrs = perrs[timeind]

    # return a dict with everything
    modeldict = {
        'vartype':'planet',
        'params':{x:np.asscalar(y) for x,y in zip(['transitperiod',
                                                   'transitepoch',
                                                   'transitdepth',
                                                   'transitduration',
                                                   'ingressduration'],
                                                  [period,
                                                   epoch,
                                                   depth,
                                                   duration,
                                                   ingduration])},
        'times':mtimes,
        'mags':mmags,
        'errs':merrs,
        # these are standard keys that help with later characterization of
        # variability as a function period, variability amplitude, object mag,
        # ndet, etc.
        'varperiod':period,
        'varamplitude':depth
    }

    return modeldict