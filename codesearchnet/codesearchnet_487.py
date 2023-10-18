def plot_best(trace=None, data_train=None, data_test=None,
              samples=1000, burn=200, axs=None):
    """
    Plot BEST significance analysis.

    Parameters
    ----------
    trace : pymc3.sampling.BaseTrace, optional
        trace object as returned by model_best()
        If not passed, will run model_best(), for which
        data_train and data_test are required.
    data_train : pandas.Series, optional
        Returns of in-sample period.
        Required if trace=None.
    data_test : pandas.Series, optional
        Returns of out-of-sample period.
        Required if trace=None.
    samples : int, optional
        Posterior samples to draw.
    burn : int
        Posterior sampels to discard as burn-in.
    axs : array of matplotlib.axes objects, optional
        Plot into passed axes objects. Needs 6 axes.

    Returns
    -------
    None

    See Also
    --------
    model_best : Estimation of BEST model.
    """

    if trace is None:
        if (data_train is not None) or (data_test is not None):
            raise ValueError('Either pass trace or data_train and data_test')
        trace = model_best(data_train, data_test, samples=samples)

    trace = trace[burn:]
    if axs is None:
        fig, axs = plt.subplots(ncols=2, nrows=3, figsize=(16, 4))

    def distplot_w_perc(trace, ax):
        sns.distplot(trace, ax=ax)
        ax.axvline(
            stats.scoreatpercentile(trace, 2.5),
            color='0.5', label='2.5 and 97.5 percentiles')
        ax.axvline(
            stats.scoreatpercentile(trace, 97.5),
            color='0.5')

    sns.distplot(trace['group1_mean'], ax=axs[0], label='Backtest')
    sns.distplot(trace['group2_mean'], ax=axs[0], label='Forward')
    axs[0].legend(loc=0, frameon=True, framealpha=0.5)
    axs[1].legend(loc=0, frameon=True, framealpha=0.5)

    distplot_w_perc(trace['difference of means'], axs[1])

    axs[0].set(xlabel='Mean', ylabel='Belief', yticklabels=[])
    axs[1].set(xlabel='Difference of means', yticklabels=[])

    sns.distplot(trace['group1_annual_volatility'], ax=axs[2],
                 label='Backtest')
    sns.distplot(trace['group2_annual_volatility'], ax=axs[2],
                 label='Forward')
    distplot_w_perc(trace['group2_annual_volatility'] -
                    trace['group1_annual_volatility'], axs[3])
    axs[2].set(xlabel='Annual volatility', ylabel='Belief',
               yticklabels=[])
    axs[2].legend(loc=0, frameon=True, framealpha=0.5)
    axs[3].set(xlabel='Difference of volatility', yticklabels=[])

    sns.distplot(trace['group1_sharpe'], ax=axs[4], label='Backtest')
    sns.distplot(trace['group2_sharpe'], ax=axs[4], label='Forward')
    distplot_w_perc(trace['group2_sharpe'] - trace['group1_sharpe'],
                    axs[5])
    axs[4].set(xlabel='Sharpe', ylabel='Belief', yticklabels=[])
    axs[4].legend(loc=0, frameon=True, framealpha=0.5)
    axs[5].set(xlabel='Difference of Sharpes', yticklabels=[])

    sns.distplot(trace['effect size'], ax=axs[6])
    axs[6].axvline(
        stats.scoreatpercentile(trace['effect size'], 2.5),
        color='0.5')
    axs[6].axvline(
        stats.scoreatpercentile(trace['effect size'], 97.5),
        color='0.5')
    axs[6].set(xlabel='Difference of means normalized by volatility',
               ylabel='Belief', yticklabels=[])