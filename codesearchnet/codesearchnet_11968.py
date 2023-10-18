def phase_magseries(times, mags, period, epoch, wrap=True, sort=True):
    '''Phases a magnitude/flux time-series using a given period and epoch.

    The equation used is::

        phase = (times - epoch)/period - floor((times - epoch)/period)

    This phases the given magnitude timeseries using the given period and
    epoch. If wrap is True, wraps the result around 0.0 (and returns an array
    that has twice the number of the original elements). If sort is True,
    returns the magnitude timeseries in phase sorted order.

    Parameters
    ----------

    times,mags : np.array
        The magnitude/flux time-series values to phase using the provided
        `period` and `epoch`. Non-fiinite values will be removed.

    period : float
        The period to use to phase the time-series.

    epoch : float
        The epoch to phase the time-series. This is usually the time-of-minimum
        or time-of-maximum of some periodic light curve
        phenomenon. Alternatively, one can use the minimum time value in
        `times`.

    wrap : bool
        If this is True, the returned phased time-series will be wrapped around
        phase 0.0, which is useful for plotting purposes. The arrays returned
        will have twice the number of input elements because of this wrapping.

    sort : bool
        If this is True, the returned phased time-series will be sorted in
        increasing phase order.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'phase': the phase values,
             'mags': the mags/flux values at each phase,
             'period': the input `period` used to phase the time-series,
             'epoch': the input `epoch` used to phase the time-series}

    '''

    # find all the finite values of the magnitudes and times
    finiteind = np.isfinite(mags) & np.isfinite(times)

    finite_times = times[finiteind]
    finite_mags = mags[finiteind]

    magseries_phase = (
        (finite_times - epoch)/period -
        np.floor(((finite_times - epoch)/period))
    )

    outdict = {'phase':magseries_phase,
               'mags':finite_mags,
               'period':period,
               'epoch':epoch}

    if sort:
        sortorder = np.argsort(outdict['phase'])
        outdict['phase'] = outdict['phase'][sortorder]
        outdict['mags'] = outdict['mags'][sortorder]

    if wrap:
        outdict['phase'] = np.concatenate((outdict['phase']-1.0,
                                           outdict['phase']))
        outdict['mags'] = np.concatenate((outdict['mags'],
                                          outdict['mags']))

    return outdict