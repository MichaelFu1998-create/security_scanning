def model_returns_normal(data, samples=500, progressbar=True):
    """
    Run Bayesian model assuming returns are normally distributed.

    Parameters
    ----------
    returns : pandas.Series
        Series of simple returns of an algorithm or stock.
    samples : int (optional)
        Number of posterior samples to draw.

    Returns
    -------
    model : pymc.Model object
        PyMC3 model containing all random variables.
    trace : pymc3.sampling.BaseTrace object
        A PyMC3 trace object that contains samples for each parameter
        of the posterior.
    """

    with pm.Model() as model:
        mu = pm.Normal('mean returns', mu=0, sd=.01, testval=data.mean())
        sigma = pm.HalfCauchy('volatility', beta=1, testval=data.std())
        returns = pm.Normal('returns', mu=mu, sd=sigma, observed=data)
        pm.Deterministic(
            'annual volatility',
            returns.distribution.variance**.5 *
            np.sqrt(252))
        pm.Deterministic(
            'sharpe',
            returns.distribution.mean /
            returns.distribution.variance**.5 *
            np.sqrt(252))

        trace = pm.sample(samples, progressbar=progressbar)
    return model, trace