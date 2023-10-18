def model_best(y1, y2, samples=1000, progressbar=True):
    """
    Bayesian Estimation Supersedes the T-Test

    This model runs a Bayesian hypothesis comparing if y1 and y2 come
    from the same distribution. Returns are assumed to be T-distributed.

    In addition, computes annual volatility and Sharpe of in and
    out-of-sample periods.

    This model replicates the example used in:
    Kruschke, John. (2012) Bayesian estimation supersedes the t
    test. Journal of Experimental Psychology: General.

    Parameters
    ----------
    y1 : array-like
        Array of returns (e.g. in-sample)
    y2 : array-like
        Array of returns (e.g. out-of-sample)
    samples : int, optional
        Number of posterior samples to draw.

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

    y = np.concatenate((y1, y2))

    mu_m = np.mean(y)
    mu_p = 0.000001 * 1 / np.std(y)**2

    sigma_low = np.std(y) / 1000
    sigma_high = np.std(y) * 1000
    with pm.Model() as model:
        group1_mean = pm.Normal('group1_mean', mu=mu_m, tau=mu_p,
                                testval=y1.mean())
        group2_mean = pm.Normal('group2_mean', mu=mu_m, tau=mu_p,
                                testval=y2.mean())
        group1_std = pm.Uniform('group1_std', lower=sigma_low,
                                upper=sigma_high, testval=y1.std())
        group2_std = pm.Uniform('group2_std', lower=sigma_low,
                                upper=sigma_high, testval=y2.std())
        nu = pm.Exponential('nu_minus_two', 1 / 29., testval=4.) + 2.

        returns_group1 = pm.StudentT('group1', nu=nu, mu=group1_mean,
                                     lam=group1_std**-2, observed=y1)
        returns_group2 = pm.StudentT('group2', nu=nu, mu=group2_mean,
                                     lam=group2_std**-2, observed=y2)

        diff_of_means = pm.Deterministic('difference of means',
                                         group2_mean - group1_mean)
        pm.Deterministic('difference of stds',
                         group2_std - group1_std)
        pm.Deterministic('effect size', diff_of_means /
                         pm.math.sqrt((group1_std**2 +
                                       group2_std**2) / 2))

        pm.Deterministic('group1_annual_volatility',
                         returns_group1.distribution.variance**.5 *
                         np.sqrt(252))
        pm.Deterministic('group2_annual_volatility',
                         returns_group2.distribution.variance**.5 *
                         np.sqrt(252))

        pm.Deterministic('group1_sharpe', returns_group1.distribution.mean /
                         returns_group1.distribution.variance**.5 *
                         np.sqrt(252))
        pm.Deterministic('group2_sharpe', returns_group2.distribution.mean /
                         returns_group2.distribution.variance**.5 *
                         np.sqrt(252))

        trace = pm.sample(samples, progressbar=progressbar)
    return model, trace