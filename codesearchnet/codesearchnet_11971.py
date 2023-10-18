def get_transit_times(
        blsd,
        time,
        extra_maskfrac,
        trapd=None,
        nperiodint=1000
):
    '''Given a BLS period, epoch, and transit ingress/egress points (usually
    from :py:func:`astrobase.periodbase.kbls.bls_stats_singleperiod`), return
    the times within transit durations + `extra_maskfrac` of each transit.

    Optionally, can use the (more accurate) trapezoidal fit period and epoch, if
    it's passed.  Useful for inspecting individual transits, and masking them
    out if desired.

    Parameters
    ----------

    blsd : dict
        This is the dict returned by
        :py:func:`astrobase.periodbase.kbls.bls_stats_singleperiod`.

    time : np.array
        The times from the time-series of transit observations used to calculate
        the initial period.

    extra_maskfrac : float
        This is the separation from in-transit points you desire, in units of
        the transit duration. `extra_maskfrac = 0` if you just want points
        inside transit (see below).

    trapd : dict
        This is a dict returned by
        :py:func:`astrobase.lcfit.transits.traptransit_fit_magseries` containing
        the trapezoid transit model.

    nperiodint : int
        This indicates how many periods backwards/forwards to try and identify
        transits from the epochs reported in `blsd` or `trapd`.

    Returns
    -------

    (tmids_obsd, t_starts, t_ends) : tuple of np.array
        The returned items are::

            tmids_obsd (np.ndarray): best guess of transit midtimes in
            lightcurve. Has length number of transits in lightcurve.

            t_starts (np.ndarray): t_Is - extra_maskfrac*tdur, for t_Is transit
            first contact point.

            t_ends (np.ndarray): t_Is + extra_maskfrac*tdur, for t_Is transit
            first contact point.

    '''

    if trapd:
        period = trapd['fitinfo']['finalparams'][0]
        t0 = trapd['fitinfo']['fitepoch']
        transitduration_phase = trapd['fitinfo']['finalparams'][3]
        tdur = period * transitduration_phase
    else:
        period = blsd['period']
        t0 = blsd['epoch']
        tdur = (
            period *
            (blsd['transegressbin']-blsd['transingressbin'])/blsd['nphasebins']
        )
        if not blsd['transegressbin'] > blsd['transingressbin']:

            raise NotImplementedError(
                'careful of the width. '
                'this edge case must be dealt with separately.'
            )

    tmids = [t0 + ix*period for ix in range(-nperiodint,nperiodint)]

    sel = (tmids > np.nanmin(time)) & (tmids < np.nanmax(time))
    tmids_obsd = np.array(tmids)[sel]

    t_Is = tmids_obsd - tdur/2
    t_IVs = tmids_obsd + tdur/2

    # focus on the times around transit
    t_starts = t_Is - extra_maskfrac * tdur
    t_ends = t_IVs + extra_maskfrac * tdur

    return tmids_obsd, t_starts, t_ends