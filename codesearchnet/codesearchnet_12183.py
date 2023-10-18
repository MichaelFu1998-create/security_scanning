def flare_model_residual(flareparams, times, mags, errs):
    '''
    This returns the residual between model mags and the actual mags.

    Parameters
    ----------

    flareparams : list of float
        This defines the flare model::

            [amplitude,
             flare_peak_time,
             rise_gaussian_stdev,
             decay_time_constant]

        where:

        `amplitude`: the maximum flare amplitude in mags or flux. If flux, then
        amplitude should be positive. If mags, amplitude should be negative.

        `flare_peak_time`: time at which the flare maximum happens.

        `rise_gaussian_stdev`: the stdev of the gaussian describing the rise of
        the flare.

        `decay_time_constant`: the time constant of the exponential fall of the
        flare.

    times,mags,errs : np.array
        The input time-series of measurements and associated errors for which
        the model will be generated. The times will be used to generate
        model mags.

    Returns
    -------

    np.array
        The residuals between the input `mags` and generated `modelmags`,
        weighted by the measurement errors in `errs`.

    '''

    modelmags, _, _, _ = flare_model(flareparams, times, mags, errs)

    return (mags - modelmags)/errs