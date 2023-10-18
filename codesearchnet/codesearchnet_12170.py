def _legendre_dtr(x, y, y_err, legendredeg=10):
    '''This calculates the residual and chi-sq values for a Legendre
    function fit.

    Parameters
    ----------

    x : np.array
        Array of the independent variable.

    y : np.array
        Array of the dependent variable.

    y_err : np.array
        Array of errors associated with each `y` value. Used to calculate fit
        weights.

    legendredeg : int
        The degree of the Legendre function to use when fitting.

    Returns
    -------

    tuple
        The tuple returned is of the form: (fit_y, fitchisq, fitredchisq)

    '''
    try:
        p = Legendre.fit(x, y, legendredeg)
        fit_y = p(x)
    except Exception as e:
        fit_y = npzeros_like(y)

    fitchisq = npsum(
        ((fit_y - y)*(fit_y - y)) / (y_err*y_err)
    )

    nparams = legendredeg + 1
    fitredchisq = fitchisq/(len(y) - nparams - 1)

    LOGINFO(
        'legendre detrend applied. chisq = %.5f, reduced chisq = %.5f' %
        (fitchisq, fitredchisq)
    )

    return fit_y, fitchisq, fitredchisq