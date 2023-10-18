def gilliland_cdpp(times, mags, errs,
                   windowlength=97,
                   polyorder=2,
                   binsize=23400,  # in seconds: 6.5 hours for classic CDPP
                   sigclip=5.0,
                   magsarefluxes=False,
                   **kwargs):
    '''This calculates the CDPP of a timeseries using the method in the paper:

    Gilliland, R. L., Chaplin, W. J., Dunham, E. W., et al. 2011, ApJS, 197, 6
    (http://adsabs.harvard.edu/abs/2011ApJS..197....6G)

    The steps are:

    - pass the time-series through a Savitsky-Golay filter.

      - we use `scipy.signal.savgol_filter`, `**kwargs` are passed to this.

      - also see: http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay.

      - the `windowlength` is the number of LC points to use (Kepler uses 2 days
        = (1440 minutes/day / 30 minutes/LC point) x 2 days = 96 -> 97 LC
        points).

      - the `polyorder` is a quadratic by default.


    - subtract the smoothed time-series from the actual light curve.

    - sigma clip the remaining LC.

    - get the binned mag series by averaging over 6.5 hour bins, only retaining
      bins with at least 7 points.

    - the standard deviation of the binned averages is the CDPP.

    - multiply this by 1.168 to correct for over-subtraction of white-noise.


    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to calculate CDPP for.

    windowlength : int
        The smoothing window size to use.

    polyorder : int
        The polynomial order to use in the Savitsky-Golay smoothing.

    binsize : int
        The bin size to use for binning the light curve.

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
        If True, indicates the input time-series is fluxes and not mags.

    kwargs : additional kwargs
        These are passed directly to `scipy.signal.savgol_filter`.

    Returns
    -------

    float
        The calculated CDPP value.

    '''

    # if no errs are given, assume 0.1% errors
    if errs is None:
        errs = 0.001*mags

    # get rid of nans first
    find = npisfinite(times) & npisfinite(mags) & npisfinite(errs)
    ftimes = times[find]
    fmags = mags[find]
    ferrs = errs[find]

    if ftimes.size < (3*windowlength):
        LOGERROR('not enough LC points to calculate CDPP')
        return npnan

    # now get the smoothed mag series using the filter
    # kwargs are provided to the savgol_filter function
    smoothed = savgol_filter(fmags, windowlength, polyorder, **kwargs)
    subtracted = fmags - smoothed

    # sigclip the subtracted light curve
    stimes, smags, serrs = sigclip_magseries(ftimes, subtracted, ferrs,
                                             magsarefluxes=magsarefluxes)

    # bin over 6.5 hour bins and throw away all bins with less than 7 elements
    binned = time_bin_magseries_with_errs(stimes, smags, serrs,
                                          binsize=binsize,
                                          minbinelems=7)
    bmags = binned['binnedmags']

    # stdev of bin mags x 1.168 -> CDPP
    cdpp = npstd(bmags) * 1.168

    return cdpp