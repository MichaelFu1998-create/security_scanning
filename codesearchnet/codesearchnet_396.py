def adjust_returns_for_slippage(returns, positions, transactions,
                                slippage_bps):
    """
    Apply a slippage penalty for every dollar traded.

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
    slippage_bps: int/float
        Basis points of slippage to apply.

    Returns
    -------
    pd.Series
        Time series of daily returns, adjusted for slippage.
    """

    slippage = 0.0001 * slippage_bps
    portfolio_value = positions.sum(axis=1)
    pnl = portfolio_value * returns
    traded_value = get_txn_vol(transactions).txn_volume
    slippage_dollars = traded_value * slippage
    adjusted_pnl = pnl.add(-slippage_dollars, fill_value=0)
    adjusted_returns = returns * adjusted_pnl / pnl

    return adjusted_returns