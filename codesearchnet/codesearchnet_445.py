def plot_exposures(returns, positions, ax=None, **kwargs):
    """
    Plots a cake chart of the long and short exposure.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    positions_alloc : pd.DataFrame
        Portfolio allocation of positions. See
        pos.get_percent_alloc.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    pos_no_cash = positions.drop('cash', axis=1)
    l_exp = pos_no_cash[pos_no_cash > 0].sum(axis=1) / positions.sum(axis=1)
    s_exp = pos_no_cash[pos_no_cash < 0].sum(axis=1) / positions.sum(axis=1)
    net_exp = pos_no_cash.sum(axis=1) / positions.sum(axis=1)

    ax.fill_between(l_exp.index,
                    0,
                    l_exp.values,
                    label='Long', color='green', alpha=0.5)
    ax.fill_between(s_exp.index,
                    0,
                    s_exp.values,
                    label='Short', color='red', alpha=0.5)
    ax.plot(net_exp.index, net_exp.values,
            label='Net', color='black', linestyle='dotted')

    ax.set_xlim((returns.index[0], returns.index[-1]))
    ax.set_title("Exposure")
    ax.set_ylabel('Exposure')
    ax.legend(loc='lower left', frameon=True, framealpha=0.5)
    ax.set_xlabel('')
    return ax