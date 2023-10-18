def model_returns_t_alpha_beta(data, bmark, samples=2000, progressbar=True):
    """
    Run Bayesian alpha-beta-model with T distributed returns.

    This model estimates intercept (alpha) and slope (beta) of two
    return sets. Usually, these will be algorithm returns and
    benchmark returns (e.g. S&P500). The data is assumed to be T
    distributed and thus is robust to outliers and takes tail events
    into account.  If a pandas.DataFrame is passed as a benchmark, then
    multiple linear regression is used to estimate alpha and beta.

    Parameters
    ----------
    returns : pandas.Series
        Series of simple returns of an algorithm or stock.
    bmark : pandas.DataFrame
        DataFrame of benchmark returns (e.g., S&P500) or risk factors (e.g.,
        Fama-French SMB, HML, and UMD).
        If bmark has more recent returns than returns_train, these dates
        will be treated as missing values and predictions will be
        generated for them taking market correlations into account.
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

    data_bmark = pd.concat([data, bmark], axis=1).dropna()

    with pm.Model() as model:
        sigma = pm.HalfCauchy(
            'sigma',
            beta=1)
        nu = pm.Exponential('nu_minus_two', 1. / 10.)

        # alpha and beta
        X = data_bmark.iloc[:, 1]
        y = data_bmark.iloc[:, 0]

        alpha_reg = pm.Normal('alpha', mu=0, sd=.1)
        beta_reg = pm.Normal('beta', mu=0, sd=1)

        mu_reg = alpha_reg + beta_reg * X
        pm.StudentT('returns',
                    nu=nu + 2,
                    mu=mu_reg,
                    sd=sigma,
                    observed=y)
        trace = pm.sample(samples, progressbar=progressbar)

    return model, trace