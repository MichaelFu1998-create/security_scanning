def given_lc_get_out_of_transit_points(
        time, flux, err_flux,
        blsfit_savpath=None,
        trapfit_savpath=None,
        in_out_transit_savpath=None,
        sigclip=None,
        magsarefluxes=True,
        nworkers=1,
        extra_maskfrac=0.03
):
    '''This gets the out-of-transit light curve points.

    Relevant during iterative masking of transits for multiple planet system
    search.

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

    in_out_transit_savpath : str or None
        If provided as a str, indicates the path of the plot file that will be
        made for a plot showing the in-transit points and out-of-transit points
        tagged separately.

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

    (times_oot, fluxes_oot, errs_oot) : tuple of np.array
        The `times`, `flux`, `err_flux` values from the input at the time values
        out-of-transit are returned.

    '''

    tmids_obsd, t_starts, t_ends = (
        given_lc_get_transit_tmids_tstarts_tends(
            time, flux, err_flux, blsfit_savpath=blsfit_savpath,
            trapfit_savpath=trapfit_savpath, magsarefluxes=magsarefluxes,
            nworkers=nworkers, sigclip=sigclip, extra_maskfrac=extra_maskfrac
        )
    )

    in_transit = np.zeros_like(time).astype(bool)

    for t_start, t_end in zip(t_starts, t_ends):

        this_transit = ( (time > t_start) & (time < t_end) )

        in_transit |= this_transit

    out_of_transit = ~in_transit

    if in_out_transit_savpath:
        _in_out_transit_plot(time, flux, in_transit, out_of_transit,
                             in_out_transit_savpath)

    return time[out_of_transit], flux[out_of_transit], err_flux[out_of_transit]