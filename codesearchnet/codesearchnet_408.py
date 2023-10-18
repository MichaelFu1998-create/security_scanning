def plot_returns(perf_attrib_data, cost=None, ax=None):
    """
    Plot total, specific, and common returns.

    Parameters
    ----------
    perf_attrib_data : pd.DataFrame
        df with factors, common returns, and specific returns as columns,
        and datetimes as index. Assumes the `total_returns` column is NOT
        cost adjusted.
        - Example:
                        momentum  reversal  common_returns  specific_returns
            dt
            2017-01-01  0.249087  0.935925        1.185012          1.185012
            2017-01-02 -0.003194 -0.400786       -0.403980         -0.403980

    cost : pd.Series, optional
        if present, gets subtracted from `perf_attrib_data['total_returns']`,
        and gets plotted separately

    ax :  matplotlib.axes.Axes
        axes on which plots are made. if None, current axes will be used

    Returns
    -------
    ax :  matplotlib.axes.Axes
    """

    if ax is None:
        ax = plt.gca()

    returns = perf_attrib_data['total_returns']
    total_returns_label = 'Total returns'

    cumulative_returns_less_costs = _cumulative_returns_less_costs(
        returns,
        cost
    )
    if cost is not None:
        total_returns_label += ' (adjusted)'

    specific_returns = perf_attrib_data['specific_returns']
    common_returns = perf_attrib_data['common_returns']

    ax.plot(cumulative_returns_less_costs, color='b',
            label=total_returns_label)
    ax.plot(ep.cum_returns(specific_returns), color='g',
            label='Cumulative specific returns')
    ax.plot(ep.cum_returns(common_returns), color='r',
            label='Cumulative common returns')

    if cost is not None:
        ax.plot(-ep.cum_returns(cost), color='k',
                label='Cumulative cost spent')

    ax.set_title('Time series of cumulative returns')
    ax.set_ylabel('Returns')

    configure_legend(ax)

    return ax