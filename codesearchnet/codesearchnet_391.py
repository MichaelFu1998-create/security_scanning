def get_low_liquidity_transactions(transactions, market_data,
                                   last_n_days=None):
    """
    For each traded name, find the daily transaction total that consumed
    the greatest proportion of available daily bar volume.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.
    market_data : pd.Panel
        Panel with items axis of 'price' and 'volume' DataFrames.
        The major and minor axes should match those of the
        the passed positions DataFrame (same dates and symbols).
    last_n_days : integer
        Compute for only the last n days of the passed backtest data.
    """

    txn_daily_w_bar = daily_txns_with_bar_data(transactions, market_data)
    txn_daily_w_bar.index.name = 'date'
    txn_daily_w_bar = txn_daily_w_bar.reset_index()

    if last_n_days is not None:
        md = txn_daily_w_bar.date.max() - pd.Timedelta(days=last_n_days)
        txn_daily_w_bar = txn_daily_w_bar[txn_daily_w_bar.date > md]

    bar_consumption = txn_daily_w_bar.assign(
        max_pct_bar_consumed=(
            txn_daily_w_bar.amount/txn_daily_w_bar.volume)*100
    ).sort_values('max_pct_bar_consumed', ascending=False)
    max_bar_consumption = bar_consumption.groupby('symbol').first()

    return max_bar_consumption[['date', 'max_pct_bar_consumed']]