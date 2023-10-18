def simple_flare_find(times, mags, errs,
                      smoothbinsize=97,
                      flare_minsigma=4.0,
                      flare_maxcadencediff=1,
                      flare_mincadencepoints=3,
                      magsarefluxes=False,
                      savgol_polyorder=2,
                      **savgol_kwargs):
    '''This finds flares in time series using the method in Walkowicz+ 2011.

    FIXME: finish this.

    Parameters
    ----------

    times,mags,errs : np.array
        The input time-series to find flares in.

    smoothbinsize : int
        The number of consecutive light curve points to smooth over in the time
        series using a Savitsky-Golay filter. The smoothed light curve is then
        subtracted from the actual light curve to remove trends that potentially
        last `smoothbinsize` light curve points. The default value is chosen as
        ~6.5 hours (97 x 4 minute cadence for HATNet/HATSouth).

    flare_minsigma : float
        The minimum sigma above the median LC level to designate points as
        belonging to possible flares.

    flare_maxcadencediff : int
        The maximum number of light curve points apart each possible flare event
        measurement is allowed to be. If this is 1, then we'll look for
        consecutive measurements.

    flare_mincadencepoints : int
        The minimum number of light curve points (each `flare_maxcadencediff`
        points apart) required that are at least `flare_minsigma` above the
        median light curve level to call an event a flare.

    magsarefluxes: bool
        If True, indicates that mags is actually an array of fluxes.

    savgol_polyorder: int
        The polynomial order of the function used by the Savitsky-Golay filter.

    savgol_kwargs : extra kwargs
        Any remaining keyword arguments are passed directly to the
        `savgol_filter` function from `scipy.signal`.

    Returns
    -------

    (nflares, flare_indices) : tuple
        Returns the total number of flares found and their time-indices (start,
        end) as tuples.

    '''

    # if no errs are given, assume 0.1% errors
    if errs is None:
        errs = 0.001*mags

    # get rid of nans first
    finiteind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes = times[finiteind]
    fmags = mags[finiteind]
    ferrs = errs[finiteind]

    # now get the smoothed mag series using the filter
    # kwargs are provided to the savgol_filter function
    smoothed = savgol_filter(fmags,
                             smoothbinsize,
                             savgol_polyorder,
                             **savgol_kwargs)
    subtracted = fmags - smoothed

    # calculate some stats
    # the series_median is ~zero after subtraction
    series_mad = np.median(np.abs(subtracted))
    series_stdev = 1.483*series_mad

    # find extreme positive deviations
    if magsarefluxes:
        extind = np.where(subtracted > (flare_minsigma*series_stdev))
    else:
        extind = np.where(subtracted < (-flare_minsigma*series_stdev))

    # see if there are any extrema
    if extind and extind[0]:

        extrema_indices = extind[0]
        flaregroups = []

        # find the deviations within the requested flaremaxcadencediff
        for ind, extrema_index in enumerate(extrema_indices):
            # FIXME: finish this
            pass