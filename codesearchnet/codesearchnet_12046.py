def generate_eb_lightcurve(
        times,
        mags=None,
        errs=None,
        paramdists={'period':sps.uniform(loc=0.2,scale=99.8),
                    'pdepth':sps.uniform(loc=1.0e-4,scale=0.7),
                    'pduration':sps.uniform(loc=0.01,scale=0.44),
                    'depthratio':sps.uniform(loc=0.01,scale=0.99),
                    'secphase':sps.norm(loc=0.5,scale=0.1)},
        magsarefluxes=False,
):
    '''This generates fake EB light curves.

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

            {'period', 'pdepth', 'pduration', 'depthratio', 'secphase'}

        The values of these keys should all be 'frozen' scipy.stats distribution
        objects, e.g.:

        https://docs.scipy.org/doc/scipy/reference/stats.html#continuous-distributions
        The variability epoch will be automatically chosen from a uniform
        distribution between `times.min()` and `times.max()`.

        The `pdepth` will be flipped automatically as appropriate if
        `magsarefluxes=True`.

    magsarefluxes : bool
        If the generated time series is meant to be a flux time-series, set this
        to True to get the correct sign of variability amplitude.

    Returns
    -------

    dict
        A dict of the form below is returned::

            {'vartype': 'EB',
             'params': {'period': generated value of period,
                        'epoch': generated value of epoch,
                        'pdepth': generated value of priary eclipse depth,
                        'pduration': generated value of prim eclipse duration,
                        'depthratio': generated value of prim/sec eclipse
                                      depth ratio},
             'times': the model times,
             'mags': the model mags,
             'errs': the model errs,
             'varperiod': the generated period of variability == 'period'
             'varamplitude': the generated amplitude of
                             variability == 'pdepth'}

    '''

    if mags is None:
        mags = np.full_like(times, 0.0)

    if errs is None:
        errs = np.full_like(times, 0.0)

    # choose the epoch
    epoch = npr.random()*(times.max() - times.min()) + times.min()

    # choose the period, pdepth, duration, depthratio
    period = paramdists['period'].rvs(size=1)
    pdepth = paramdists['pdepth'].rvs(size=1)
    pduration = paramdists['pduration'].rvs(size=1)
    depthratio = paramdists['depthratio'].rvs(size=1)
    secphase = paramdists['secphase'].rvs(size=1)

    # fix the transit depth if it needs to be flipped
    if magsarefluxes and pdepth < 0.0:
        pdepth = -pdepth
    elif not magsarefluxes and pdepth > 0.0:
        pdepth = -pdepth

    # generate the model
    modelmags, phase, ptimes, pmags, perrs = (
        eclipses.invgauss_eclipses_func([period, epoch, pdepth,
                                         pduration, depthratio, secphase],
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
        'vartype':'EB',
        'params':{x:np.asscalar(y) for x,y in zip(['period',
                                                   'epoch',
                                                   'pdepth',
                                                   'pduration',
                                                   'depthratio'],
                                                  [period,
                                                   epoch,
                                                   pdepth,
                                                   pduration,
                                                   depthratio])},
        'times':mtimes,
        'mags':mmags,
        'errs':merrs,
        'varperiod':period,
        'varamplitude':pdepth,
    }

    return modeldict