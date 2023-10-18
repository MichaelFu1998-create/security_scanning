def run_model(model, returns_train, returns_test=None,
              bmark=None, samples=500, ppc=False, progressbar=True):
    """
    Run one of the Bayesian models.

    Parameters
    ----------
    model : {'alpha_beta', 't', 'normal', 'best'}
        Which model to run
    returns_train : pd.Series
        Timeseries of simple returns
    returns_test : pd.Series (optional)
        Out-of-sample returns. Datetimes in returns_test will be added to
        returns_train as missing values and predictions will be generated
        for them.
    bmark : pd.Series or pd.DataFrame (optional)
        Only used for alpha_beta to estimate regression coefficients.
        If bmark has more recent returns than returns_train, these dates
        will be treated as missing values and predictions will be
        generated for them taking market correlations into account.
    samples : int (optional)
        Number of posterior samples to draw.
    ppc : boolean (optional)
        Whether to run a posterior predictive check. Will generate
        samples of length returns_test.  Returns a second argument
        that contains the PPC of shape samples x len(returns_test).

    Returns
    -------
    trace : pymc3.sampling.BaseTrace object
        A PyMC3 trace object that contains samples for each parameter
        of the posterior.

    ppc : numpy.array (if ppc==True)
       PPC of shape samples x len(returns_test).
    """

    if model == 'alpha_beta':
        model, trace = model_returns_t_alpha_beta(returns_train,
                                                  bmark, samples,
                                                  progressbar=progressbar)
    elif model == 't':
        model, trace = model_returns_t(returns_train, samples,
                                       progressbar=progressbar)
    elif model == 'normal':
        model, trace = model_returns_normal(returns_train, samples,
                                            progressbar=progressbar)
    elif model == 'best':
        model, trace = model_best(returns_train, returns_test,
                                  samples=samples,
                                  progressbar=progressbar)
    else:
        raise NotImplementedError(
            'Model {} not found.'
            'Use alpha_beta, t, normal, or best.'.format(model))

    if ppc:
        ppc_samples = pm.sample_ppc(trace, samples=samples,
                                    model=model, size=len(returns_test),
                                    progressbar=progressbar)
        return trace, ppc_samples['returns']

    return trace