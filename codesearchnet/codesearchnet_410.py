def plot_factor_contribution_to_perf(
        perf_attrib_data,
        ax=None,
        title='Cumulative common returns attribution',
):
    """
    Plot each factor's contribution to performance.

    Parameters
    ----------
    perf_attrib_data : pd.DataFrame
        df with factors, common returns, and specific returns as columns,
        and datetimes as index
        - Example:
                        momentum  reversal  common_returns  specific_returns
            dt
            2017-01-01  0.249087  0.935925        1.185012          1.185012
            2017-01-02 -0.003194 -0.400786       -0.403980         -0.403980

    ax :  matplotlib.axes.Axes
        axes on which plots are made. if None, current axes will be used

    title : str, optional
        title of plot

    Returns
    -------
    ax :  matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    factors_to_plot = perf_attrib_data.drop(
        ['total_returns', 'common_returns'], axis='columns', errors='ignore'
    )

    factors_cumulative = pd.DataFrame()
    for factor in factors_to_plot:
        factors_cumulative[factor] = ep.cum_returns(factors_to_plot[factor])

    for col in factors_cumulative:
        ax.plot(factors_cumulative[col])

    ax.axhline(0, color='k')
    configure_legend(ax, change_colors=True)

    ax.set_ylabel('Cumulative returns by factor')
    ax.set_title(title)

    return ax