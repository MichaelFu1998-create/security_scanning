def plot_return_quantiles(returns, live_start_date=None, ax=None, **kwargs):
    """
    Creates a box plot of daily, weekly, and monthly return
    distributions.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    live_start_date : datetime, optional
        The point in time when the strategy began live trading, after
        its backtest period.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to seaborn plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    is_returns = returns if live_start_date is None \
        else returns.loc[returns.index < live_start_date]
    is_weekly = ep.aggregate_returns(is_returns, 'weekly')
    is_monthly = ep.aggregate_returns(is_returns, 'monthly')
    sns.boxplot(data=[is_returns, is_weekly, is_monthly],
                palette=["#4c72B0", "#55A868", "#CCB974"],
                ax=ax, **kwargs)

    if live_start_date is not None:
        oos_returns = returns.loc[returns.index >= live_start_date]
        oos_weekly = ep.aggregate_returns(oos_returns, 'weekly')
        oos_monthly = ep.aggregate_returns(oos_returns, 'monthly')

        sns.swarmplot(data=[oos_returns, oos_weekly, oos_monthly], ax=ax,
                      color="red",
                      marker="d", **kwargs)
        red_dots = matplotlib.lines.Line2D([], [], color="red", marker="d",
                                           label="Out-of-sample data",
                                           linestyle='')
        ax.legend(handles=[red_dots], frameon=True, framealpha=0.5)
    ax.set_xticklabels(['Daily', 'Weekly', 'Monthly'])
    ax.set_title('Return quantiles')

    return ax