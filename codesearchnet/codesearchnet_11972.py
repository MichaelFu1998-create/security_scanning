def given_lc_get_transit_tmids_tstarts_tends(
        time,
        flux,
        err_flux,
        blsfit_savpath=None,
        trapfit_savpath=None,
        magsarefluxes=True,
        nworkers=1,
        sigclip=None,
        extra_maskfrac=0.03
):
    '''Gets the transit start, middle, and end times for transits in a given
    time-series of observations.

    Parameters
    ----------

    time,flux,err_flux : np.array
        The input flux time-series measurements and their associated measurement
        errors

    blsfit_savpath : str or None
        If provided as a str, indicates the path of the fit plot to make for a
        simple BLS model fit to the transit using the obtained period and epoch.

    trapfit_savpath : str or None
        If provided as a str, indicates the path of the fit plot to make for a
        trapezoidal transit model fit to the transit using the obtained period
        and epoch.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    magsarefluxes : bool
        This is by default True for this function, since it works on fluxes only
        at the moment.

    nworkers : int
        The number of parallel BLS period-finder workers to use.

    extra_maskfrac : float
        This is the separation (N) from in-transit points you desire, in units
        of the transit duration. `extra_maskfrac = 0` if you just want points
        inside transit, otherwise::

            t_starts = t_Is - N*tdur, t_ends = t_IVs + N*tdur

        Thus setting N=0.03 masks slightly more than the guessed transit
        duration.

    Returns
    -------

    (tmids_obsd, t_starts, t_ends) : tuple
        The returned items are::

            tmids_obsd (np.ndarray): best guess of transit midtimes in
            lightcurve. Has length number of transits in lightcurve.

            t_starts (np.ndarray): t_Is - extra_maskfrac*tdur, for t_Is transit
            first contact point.

            t_ends (np.ndarray): t_Is + extra_maskfrac*tdur, for t_Is transit
            first contact point.

    '''

    # first, run BLS to get an initial epoch and period.
    endp = 1.05*(np.nanmax(time) - np.nanmin(time))/2

    blsdict = kbls.bls_parallel_pfind(time, flux, err_flux,
                                      magsarefluxes=magsarefluxes, startp=0.1,
                                      endp=endp, maxtransitduration=0.3,
                                      nworkers=nworkers, sigclip=sigclip)

    blsd = kbls.bls_stats_singleperiod(time, flux, err_flux,
                                       blsdict['bestperiod'],
                                       magsarefluxes=True, sigclip=sigclip,
                                       perioddeltapercent=5)
    #  plot the BLS model.
    if blsfit_savpath:
        make_fit_plot(blsd['phases'], blsd['phasedmags'], None,
                      blsd['blsmodel'], blsd['period'], blsd['epoch'],
                      blsd['epoch'], blsfit_savpath,
                      magsarefluxes=magsarefluxes)

    ingduration_guess = blsd['transitduration'] * 0.2  # a guesstimate.
    transitparams = [
        blsd['period'], blsd['epoch'], blsd['transitdepth'],
        blsd['transitduration'], ingduration_guess
    ]

    # fit a trapezoidal transit model; plot the resulting phased LC.
    if trapfit_savpath:
        trapd = traptransit_fit_magseries(time, flux, err_flux,
                                          transitparams,
                                          magsarefluxes=magsarefluxes,
                                          sigclip=sigclip,
                                          plotfit=trapfit_savpath)

    # use the trapezoidal model's epoch as the guess to identify (roughly) in
    # and out of transit points
    tmids, t_starts, t_ends = get_transit_times(blsd,
                                                time,
                                                extra_maskfrac,
                                                trapd=trapd)

    return tmids, t_starts, t_ends