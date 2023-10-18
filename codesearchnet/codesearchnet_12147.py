def epd_magseries(times, mags, errs,
                  fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd,
                  magsarefluxes=False,
                  epdsmooth_sigclip=3.0,
                  epdsmooth_windowsize=21,
                  epdsmooth_func=smooth_magseries_savgol,
                  epdsmooth_extraparams=None):
    '''Detrends a magnitude series using External Parameter Decorrelation.

    Requires a set of external parameters similar to those present in HAT light
    curves. At the moment, the HAT light-curve-specific external parameters are:

    - S: the 'fsv' column in light curves,
    - D: the 'fdv' column in light curves,
    - K: the 'fkv' column in light curves,
    - x coords: the 'xcc' column in light curves,
    - y coords: the 'ycc' column in light curves,
    - background value: the 'bgv' column in light curves,
    - background error: the 'bge' column in light curves,
    - hour angle: the 'iha' column in light curves,
    - zenith distance: the 'izd' column in light curves

    S, D, and K are defined as follows:

    - S -> measure of PSF sharpness (~1/sigma^2 sosmaller S = wider PSF)
    - D -> measure of PSF ellipticity in xy direction
    - K -> measure of PSF ellipticity in cross direction

    S, D, K are related to the PSF's variance and covariance, see eqn 30-33 in
    A. Pal's thesis: https://arxiv.org/abs/0906.3486

    NOTE: The errs are completely ignored and returned unchanged (except for
    sigclip and finite filtering).

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to detrend.

    fsv : np.array
        Array containing the external parameter `S` of the same length as times.

    fdv : np.array
        Array containing the external parameter `D` of the same length as times.

    fkv : np.array
        Array containing the external parameter `K` of the same length as times.

    xcc : np.array
        Array containing the external parameter `x-coords` of the same length as
        times.

    ycc : np.array
        Array containing the external parameter `y-coords` of the same length as
        times.

    bgv : np.array
        Array containing the external parameter `background value` of the same
        length as times.

    bge : np.array
        Array containing the external parameter `background error` of the same
        length as times.

    iha : np.array
        Array containing the external parameter `hour angle` of the same length
        as times.

    izd : np.array
        Array containing the external parameter `zenith distance` of the same
        length as times.

    magsarefluxes : bool
        Set this to True if `mags` actually contains fluxes.

    epdsmooth_sigclip : float or int or sequence of two floats/ints or None
        This specifies how to sigma-clip the input LC before fitting the EPD
        function to it.

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

    epdsmooth_windowsize : int
        This is the number of LC points to smooth over to generate a smoothed
        light curve that will be used to fit the EPD function.

    epdsmooth_func : Python function
        This sets the smoothing filter function to use. A Savitsky-Golay filter
        is used to smooth the light curve by default. The functions that can be
        used with this kwarg are listed in `varbase.trends`. If you want to use
        your own function, it MUST have the following signature::

                def smoothfunc(mags_array, window_size, **extraparams)

        and return a numpy array of the same size as `mags_array` with the
        smoothed time-series. Any extra params can be provided using the
        `extraparams` dict.

    epdsmooth_extraparams : dict
        This is a dict of any extra filter params to supply to the smoothing
        function.

    Returns
    -------

    dict
        Returns a dict of the following form::

            {'times':the input times after non-finite elems removed,
             'mags':the EPD detrended mag values (the EPD mags),
             'errs':the errs after non-finite elems removed,
             'fitcoeffs':EPD fit coefficient values,
             'fitinfo':the full tuple returned by scipy.leastsq,
             'fitmags':the EPD fit function evaluated at times,
             'mags_median': this is median of the EPD mags,
             'mags_mad': this is the MAD of EPD mags}

    '''

    finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[::][finind], mags[::][finind], errs[::][finind]
    ffsv, ffdv, ffkv, fxcc, fycc, fbgv, fbge, fiha, fizd = (
        fsv[::][finind],
        fdv[::][finind],
        fkv[::][finind],
        xcc[::][finind],
        ycc[::][finind],
        bgv[::][finind],
        bge[::][finind],
        iha[::][finind],
        izd[::][finind],
    )

    stimes, smags, serrs, separams = sigclip_magseries_with_extparams(
        times, mags, errs,
        [fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd],
        sigclip=epdsmooth_sigclip,
        magsarefluxes=magsarefluxes
    )
    sfsv, sfdv, sfkv, sxcc, sycc, sbgv, sbge, siha, sizd = separams

    # smooth the signal
    if isinstance(epdsmooth_extraparams, dict):
        smoothedmags = epdsmooth_func(smags,
                                      epdsmooth_windowsize,
                                      **epdsmooth_extraparams)
    else:
        smoothedmags = epdsmooth_func(smags, epdsmooth_windowsize)

    # initial fit coeffs
    initcoeffs = np.zeros(22)

    # fit the smoothed mags and find the EPD function coefficients
    leastsqfit = leastsq(_epd_residual,
                         initcoeffs,
                         args=(smoothedmags,
                               sfsv, sfdv, sfkv, sxcc,
                               sycc, sbgv, sbge, siha, sizd),
                         full_output=True)

    # if the fit succeeds, then get the EPD mags
    if leastsqfit[-1] in (1,2,3,4):

        fitcoeffs = leastsqfit[0]
        epdfit = _epd_function(fitcoeffs,
                               ffsv, ffdv, ffkv, fxcc, fycc,
                               fbgv, fbge, fiha, fizd)

        epdmags = npmedian(fmags) + fmags - epdfit

        retdict = {'times':ftimes,
                   'mags':epdmags,
                   'errs':ferrs,
                   'fitcoeffs':fitcoeffs,
                   'fitinfo':leastsqfit,
                   'fitmags':epdfit,
                   'mags_median':npmedian(epdmags),
                   'mags_mad':npmedian(npabs(epdmags - npmedian(epdmags)))}

        return retdict

    # if the solution fails, return nothing
    else:

        LOGERROR('EPD fit did not converge')
        return None