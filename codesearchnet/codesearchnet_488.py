def model_stoch_vol(data, samples=2000, progressbar=True):
    """
    Run stochastic volatility model.

    This model estimates the volatility of a returns series over time.
    Returns are assumed to be T-distributed. lambda (width of
    T-distributed) is assumed to follow a random-walk.

    Parameters
    ----------
    data : pandas.Series
        Return series to model.
    samples : int, optional
        Posterior samples to draw.

    Returns
    -------
    model : pymc.Model object
        PyMC3 model containing all random variables.
    trace : pymc3.sampling.BaseTrace object
        A PyMC3 trace object that contains samples for each parameter
        of the posterior.

    See Also
    --------
    plot_stoch_vol : plotting of tochastic volatility model
    """

    from pymc3.distributions.timeseries import GaussianRandomWalk

    with pm.Model() as model:
        nu = pm.Exponential('nu', 1. / 10, testval=5.)
        sigma = pm.Exponential('sigma', 1. / .02, testval=.1)
        s = GaussianRandomWalk('s', sigma**-2, shape=len(data))
        volatility_process = pm.Deterministic('volatility_process',
                                              pm.math.exp(-2 * s))
        pm.StudentT('r', nu, lam=volatility_process, observed=data)

        trace = pm.sample(samples, progressbar=progressbar)

    return model, trace