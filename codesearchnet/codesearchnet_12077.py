def trapezoid_transit_residual(transitparams, times, mags, errs):
    '''
    This returns the residual between the modelmags and the actual mags.

    Parameters
    ----------

    transitparams : list of float
        This contains the transiting planet trapezoid model::

            transitparams = [transitperiod (time),
                             transitepoch (time),
                             transitdepth (flux or mags),
                             transitduration (phase),
                             ingressduration (phase)]

        All of these will then have fitted values after the fit is done.

        - for magnitudes -> `transitdepth` should be < 0
        - for fluxes     -> `transitdepth` should be > 0

    times,mags,errs : np.array
        The input time-series of measurements and associated errors for which
        the transit model will be generated. The times will be used to generate
        model mags, and the input `times`, `mags`, and `errs` will be resorted
        by model phase and returned.

    Returns
    -------

    np.array
        The residuals between the input `mags` and generated `modelmags`,
        weighted by the measurement errors in `errs`.


    '''

    modelmags, phase, ptimes, pmags, perrs = (
        trapezoid_transit_func(transitparams, times, mags, errs)
    )

    # this is now a weighted residual taking into account the measurement err
    return (pmags - modelmags)/perrs