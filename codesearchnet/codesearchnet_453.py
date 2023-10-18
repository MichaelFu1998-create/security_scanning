def plot_daily_turnover_hist(transactions, positions,
                             ax=None, **kwargs):
    """
    Plots a histogram of daily turnover rates.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in tears.create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
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

    if ax is None:
        ax = plt.gca()
    turnover = txn.get_turnover(positions, transactions)
    sns.distplot(turnover, ax=ax, **kwargs)
    ax.set_title('Distribution of daily turnover rates')
    ax.set_xlabel('Turnover rate')
    return ax