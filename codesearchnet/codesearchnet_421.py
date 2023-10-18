def estimate_intraday(returns, positions, transactions, EOD_hour=23):
    """
    Intraday strategies will often not hold positions at the day end.
    This attempts to find the point in the day that best represents
    the activity of the strategy on that day, and effectively resamples
    the end-of-day positions with the positions at this point of day.
    The point of day is found by detecting when our exposure in the
    market is at its maximum point. Note that this is an estimate.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.

    Returns
    -------
    pd.DataFrame
        Daily net position values, resampled for intraday behavior.
    """

    # Construct DataFrame of transaction amounts
    txn_val = transactions.copy()
    txn_val.index.names = ['date']
    txn_val['value'] = txn_val.amount * txn_val.price
    txn_val = txn_val.reset_index().pivot_table(
        index='date', values='value',
        columns='symbol').replace(np.nan, 0)

    # Cumulate transaction amounts each day
    txn_val['date'] = txn_val.index.date
    txn_val = txn_val.groupby('date').cumsum()

    # Calculate exposure, then take peak of exposure every day
    txn_val['exposure'] = txn_val.abs().sum(axis=1)
    condition = (txn_val['exposure'] == txn_val.groupby(
        pd.TimeGrouper('24H'))['exposure'].transform(max))
    txn_val = txn_val[condition].drop('exposure', axis=1)

    # Compute cash delta
    txn_val['cash'] = -txn_val.sum(axis=1)

    # Shift EOD positions to positions at start of next trading day
    positions_shifted = positions.copy().shift(1).fillna(0)
    starting_capital = positions.iloc[0].sum() / (1 + returns[0])
    positions_shifted.cash[0] = starting_capital

    # Format and add start positions to intraday position changes
    txn_val.index = txn_val.index.normalize()
    corrected_positions = positions_shifted.add(txn_val, fill_value=0)
    corrected_positions.index.name = 'period_close'
    corrected_positions.columns.name = 'sid'

    return corrected_positions