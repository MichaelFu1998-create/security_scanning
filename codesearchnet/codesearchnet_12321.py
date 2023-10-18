def fourier_sinusoidal_residual(fourierparams, times, mags, errs):
    '''
    This returns the residual between the model mags and the actual mags.

    Parameters
    ----------

    fourierparams : list
        This MUST be a list of the following form like so::

            [period,
             epoch,
             [amplitude_1, amplitude_2, amplitude_3, ..., amplitude_X],
             [phase_1, phase_2, phase_3, ..., phase_X]]

        where X is the Fourier order.

    times,mags,errs : np.array
        The input time-series of measurements and associated errors for which
        the model will be generated. The times will be used to generate model
        mags, and the input `times`, `mags`, and `errs` will be resorted by
        model phase and returned.

    Returns
    -------

    np.array
        The residuals between the input `mags` and generated `modelmags`,
        weighted by the measurement errors in `errs`.


    '''
    modelmags, phase, ptimes, pmags, perrs = (
        fourier_sinusoidal_func(fourierparams, times, mags, errs)
    )

    # this is now a weighted residual taking into account the measurement err
    return (pmags - modelmags)/perrs