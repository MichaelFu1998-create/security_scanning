def plot_monthly_returns_timeseries(returns, ax=None, **kwargs):
    """
    Plots monthly returns as a timeseries.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to seaborn plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    def cumulate_returns(x):
        return ep.cum_returns(x)[-1]

    if ax is None:
        ax = plt.gca()

    monthly_rets = returns.resample('M').apply(lambda x: cumulate_returns(x))
    monthly_rets = monthly_rets.to_period()

    sns.barplot(x=monthly_rets.index,
                y=monthly_rets.values,
                color='steelblue')

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    # only show x-labels on year boundary
    xticks_coord = []
    xticks_label = []
    count = 0
    for i in monthly_rets.index:
        if i.month == 1:
            xticks_label.append(i)
            xticks_coord.append(count)
            # plot yearly boundary line
            ax.axvline(count, color='gray', ls='--', alpha=0.3)

        count += 1

    ax.axhline(0.0, color='darkgray', ls='-')
    ax.set_xticks(xticks_coord)
    ax.set_xticklabels(xticks_label)

    return ax