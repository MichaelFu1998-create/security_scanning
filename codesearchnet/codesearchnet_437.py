def plot_perf_stats(returns, factor_returns, ax=None):
    """
    Create box plot of some performance metrics of the strategy.
    The width of the box whiskers is determined by a bootstrap.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    bootstrap_values = timeseries.perf_stats_bootstrap(returns,
                                                       factor_returns,
                                                       return_stats=False)
    bootstrap_values = bootstrap_values.drop('Kurtosis', axis='columns')

    sns.boxplot(data=bootstrap_values, orient='h', ax=ax)

    return ax