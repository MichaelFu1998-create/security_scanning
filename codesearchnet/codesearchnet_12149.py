def rfepd_magseries(times, mags, errs,
                    externalparam_arrs,
                    magsarefluxes=False,
                    epdsmooth=True,
                    epdsmooth_sigclip=3.0,
                    epdsmooth_windowsize=21,
                    epdsmooth_func=smooth_magseries_savgol,
                    epdsmooth_extraparams=None,
                    rf_subsample=1.0,
                    rf_ntrees=300,
                    rf_extraparams={'criterion':'mse',
                                    'oob_score':False,
                                    'n_jobs':-1}):
    '''This uses a `RandomForestRegressor` to de-correlate the given magseries.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to run EPD on.

    externalparam_arrs : list of np.arrays
        This is a list of ndarrays of external parameters to decorrelate
        against. These should all be the same size as `times`, `mags`, `errs`.

    epdsmooth : bool
        If True, sets the training LC for the RandomForestRegress to be a
        smoothed version of the sigma-clipped light curve provided in `times`,
        `mags`, `errs`.

    epdsmooth_sigclip : float or int or sequence of two floats/ints or None
        This specifies how to sigma-clip the input LC before smoothing it and
        fitting the EPD function to it. The actual LC will not be sigma-clipped.

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

    rf_subsample : float
        Defines the fraction of the size of the `mags` array to use for
        training the random forest regressor.

    rf_ntrees : int
        This is the number of trees to use for the `RandomForestRegressor`.

    rf_extraprams : dict
        This is a dict of any extra kwargs to provide to the
        `RandomForestRegressor` instance used.

    Returns
    -------

    dict
        Returns a dict with decorrelated mags and the usual info from the
        `RandomForestRegressor`: variable importances, etc.

    '''

    # get finite times, mags, errs
    finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[::][finind], mags[::][finind], errs[::][finind]
    finalparam_arrs = []
    for ep in externalparam_arrs:
        finalparam_arrs.append(ep[::][finind])

    stimes, smags, serrs, eparams = sigclip_magseries_with_extparams(
        times, mags, errs,
        externalparam_arrs,
        sigclip=epdsmooth_sigclip,
        magsarefluxes=magsarefluxes
    )

    # smoothing is optional for RFR because we train on a fraction of the mag
    # series and so should not require a smoothed input to fit a function to
    if epdsmooth:

        # smooth the signal
        if isinstance(epdsmooth_extraparams, dict):
            smoothedmags = epdsmooth_func(smags,
                                          epdsmooth_windowsize,
                                          **epdsmooth_extraparams)
        else:
            smoothedmags = epdsmooth_func(smags,
                                          epdsmooth_windowsize)

    else:

        smoothedmags = smags


    # set up the regressor
    if isinstance(rf_extraparams, dict):
        RFR = RandomForestRegressor(n_estimators=rf_ntrees,
                                    **rf_extraparams)
    else:
        RFR = RandomForestRegressor(n_estimators=rf_ntrees)

    # collect the features
    features = np.column_stack(eparams)

    # fit, then generate the predicted values, then get corrected values

    # we fit on a randomly selected subsample of all the mags
    if rf_subsample < 1.0:
        featureindices = np.arange(smoothedmags.size)

        # these are sorted because time-order should be important
        training_indices = np.sort(
            npr.choice(featureindices,
                       size=int(rf_subsample*smoothedmags.size),
                       replace=False)
        )
    else:
        training_indices = np.arange(smoothedmags.size)

    RFR.fit(features[training_indices,:], smoothedmags[training_indices])

    # predict on the full feature set
    flux_corrections = RFR.predict(np.column_stack(finalparam_arrs))
    corrected_fmags = npmedian(fmags) + fmags - flux_corrections

    retdict = {'times':ftimes,
               'mags':corrected_fmags,
               'errs':ferrs,
               'feature_importances':RFR.feature_importances_,
               'regressor':RFR,
               'mags_median':npmedian(corrected_fmags),
               'mags_mad':npmedian(npabs(corrected_fmags -
                                         npmedian(corrected_fmags)))}

    return retdict