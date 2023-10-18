def plot_daily_volume(returns, transactions, ax=None, **kwargs):
    """
    Plots trading volume per day vs. date.

    Also displays all-time daily average.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in tears.create_full_tear_sheet.
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
    daily_txn = txn.get_txn_vol(transactions)
    daily_txn.txn_shares.plot(alpha=1.0, lw=0.5, ax=ax, **kwargs)
    ax.axhline(daily_txn.txn_shares.mean(), color='steelblue',
               linestyle='--', lw=3, alpha=1.0)
    ax.set_title('Daily trading volume')
    ax.set_xlim((returns.index[0], returns.index[-1]))
    ax.set_ylabel('Amount of shares traded')
    ax.set_xlabel('')
    return ax