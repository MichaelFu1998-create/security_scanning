def epd_magseries_extparams(
        times,
        mags,
        errs,
        externalparam_arrs,
        initial_coeff_guess,
        magsarefluxes=False,
        epdsmooth_sigclip=3.0,
        epdsmooth_windowsize=21,
        epdsmooth_func=smooth_magseries_savgol,
        epdsmooth_extraparams=None,
        objective_func=_epd_residual2,
        objective_kwargs=None,
        optimizer_func=least_squares,
        optimizer_kwargs=None,
):
    '''This does EPD on a mag-series with arbitrary external parameters.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to run EPD on.

    externalparam_arrs : list of np.arrays
        This is a list of ndarrays of external parameters to decorrelate
        against. These should all be the same size as `times`, `mags`, `errs`.

    initial_coeff_guess : np.array
        An array of initial fit coefficients to pass into the objective
        function.

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

    objective_func : Python function
        The function that calculates residuals between the model and the
        smoothed mag-series. This must have the following signature::

            def objective_func(fit_coeffs,
                               times,
                               mags,
                               errs,
                               *external_params,
                               **objective_kwargs)

        where `times`, `mags`, `errs` are arrays of the sigma-clipped and
        smoothed time-series, `fit_coeffs` is an array of EPD fit coefficients,
        `external_params` is a tuple of the passed in external parameter arrays,
        and `objective_kwargs` is a dict of any optional kwargs to pass into the
        objective function.

        This should return the value of the residual based on evaluating the
        model function (and any weights based on errs or times).

    objective_kwargs : dict or None
        A dict of kwargs to pass into the `objective_func` function.

    optimizer_func : Python function
        The function that minimizes the residual between the model and the
        smoothed mag-series using the `objective_func`. This should have a
        signature similar to one of the optimizer functions in `scipy.optimize
        <https://docs.scipy.org/doc/scipy/reference/optimize.html>`_, i.e.::

            def optimizer_func(objective_func, initial_coeffs, args=(), ...)

        and return a `scipy.optimize.OptimizeResult
        <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html>`_. We'll
        rely on the ``.success`` attribute to determine if the EPD fit was
        successful, and the ``.x`` attribute to get the values of the fit
        coefficients.

    optimizer_kwargs : dict or None
        A dict of kwargs to pass into the `optimizer_func` function.

    Returns
    -------

    dict
        Returns a dict of the following form::

            {'times':the input times after non-finite elems removed,
             'mags':the EPD detrended mag values (the EPD mags),
             'errs':the errs after non-finite elems removed,
             'fitcoeffs':EPD fit coefficient values,
             'fitinfo':the result returned by the optimizer function,
             'mags_median': this is the median of the EPD mags,
             'mags_mad': this is the MAD of EPD mags}

    '''

    # get finite times, mags, errs
    finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[::][finind], mags[::][finind], errs[::][finind]
    finalparam_arrs = []
    for ep in externalparam_arrs:
        finalparam_arrs.append(ep[::][finind])

    # sigclip the LC to pass into the smoothing for EPD fit
    stimes, smags, serrs, eparams = sigclip_magseries_with_extparams(
        times.copy(), mags.copy(), errs.copy(),
        [x.copy() for x in externalparam_arrs],
        sigclip=epdsmooth_sigclip,
        magsarefluxes=magsarefluxes
    )

    # smooth the signal before fitting the function to it
    if isinstance(epdsmooth_extraparams, dict):
        smoothedmags = epdsmooth_func(smags,
                                      epdsmooth_windowsize,
                                      **epdsmooth_extraparams)
    else:
        smoothedmags = epdsmooth_func(smags,
                                      epdsmooth_windowsize)

    # the initial coeffs are passed in here
    initial_coeffs = initial_coeff_guess

    # reform the objective function with any optional kwargs
    if objective_kwargs is not None:
        obj_func = partial(objective_func, **objective_kwargs)
    else:
        obj_func = objective_func

    # run the optimizer function by passing in the objective function, the
    # coeffs, and the smoothed mags and external params as part of the `args`
    # tuple
    if not optimizer_kwargs:
        optimizer_kwargs = {}

    fit_info = optimizer_func(
        obj_func,
        initial_coeffs,
        args=(stimes, smoothedmags, serrs, *eparams),
        **optimizer_kwargs
    )

    if fit_info.success:

        fit_coeffs = fit_info.x

        epd_mags = np.median(fmags) + obj_func(fit_coeffs,
                                               ftimes,
                                               fmags,
                                               ferrs,
                                               *finalparam_arrs)

        retdict = {'times':ftimes,
                   'mags':epd_mags,
                   'errs':ferrs,
                   'fitcoeffs':fit_coeffs,
                   'fitinfo':fit_info,
                   'mags_median':npmedian(epd_mags),
                   'mags_mad':npmedian(npabs(epd_mags - npmedian(epd_mags)))}

        return retdict

    # if the solution fails, return nothing
    else:

        LOGERROR('EPD fit did not converge')
        return None