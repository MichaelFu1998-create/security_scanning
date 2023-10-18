def plot_bayes_cone(returns_train, returns_test, ppc,
                    plot_train_len=50, ax=None):
    """
    Generate cumulative returns plot with Bayesian cone.

    Parameters
    ----------
    returns_train : pd.Series
        Timeseries of simple returns
    returns_test : pd.Series
        Out-of-sample returns. Datetimes in returns_test will be added to
        returns_train as missing values and predictions will be generated
        for them.
    ppc : np.array
        Posterior predictive samples of shape samples x
        len(returns_test).
    plot_train_len : int (optional)
        How many data points to plot of returns_train. Useful to zoom in on
        the prediction if there is a long backtest period.
    ax : matplotlib.Axis (optional)
        Axes upon which to plot.

    Returns
    -------
    score : float
        Consistency score (see compute_consistency_score)
    trace : pymc3.sampling.BaseTrace
        A PyMC3 trace object that contains samples for each parameter
        of the posterior.
    """

    score = compute_consistency_score(returns_test,
                                      ppc)

    ax = _plot_bayes_cone(
        returns_train,
        returns_test,
        ppc,
        plot_train_len=plot_train_len,
        ax=ax)
    ax.text(
        0.40,
        0.90,
        'Consistency score: %.1f' %
        score,
        verticalalignment='bottom',
        horizontalalignment='right',
        transform=ax.transAxes,
    )

    ax.set_ylabel('Cumulative returns')
    return score