def plot_txn_time_hist(transactions, bin_minutes=5, tz='America/New_York',
                       ax=None, **kwargs):
    """
    Plots a histogram of transaction times, binning the times into
    buckets of a given duration.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in tears.create_full_tear_sheet.
    bin_minutes : float, optional
        Sizes of the bins in minutes, defaults to 5 minutes.
    tz : str, optional
        Time zone to plot against. Note that if the specified
        zone does not apply daylight savings, the distribution
        may be partially offset.
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

    txn_time = transactions.copy()

    txn_time.index = txn_time.index.tz_convert(pytz.timezone(tz))
    txn_time.index = txn_time.index.map(lambda x: x.hour * 60 + x.minute)
    txn_time['trade_value'] = (txn_time.amount * txn_time.price).abs()
    txn_time = txn_time.groupby(level=0).sum().reindex(index=range(570, 961))
    txn_time.index = (txn_time.index / bin_minutes).astype(int) * bin_minutes
    txn_time = txn_time.groupby(level=0).sum()

    txn_time['time_str'] = txn_time.index.map(lambda x:
                                              str(datetime.time(int(x / 60),
                                                                x % 60))[:-3])

    trade_value_sum = txn_time.trade_value.sum()
    txn_time.trade_value = txn_time.trade_value.fillna(0) / trade_value_sum

    ax.bar(txn_time.index, txn_time.trade_value, width=bin_minutes, **kwargs)

    ax.set_xlim(570, 960)
    ax.set_xticks(txn_time.index[::int(30 / bin_minutes)])
    ax.set_xticklabels(txn_time.time_str[::int(30 / bin_minutes)])
    ax.set_title('Transaction time distribution')
    ax.set_ylabel('Proportion')
    ax.set_xlabel('')
    return ax