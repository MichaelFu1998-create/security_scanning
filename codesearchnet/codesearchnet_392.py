def apply_slippage_penalty(returns, txn_daily, simulate_starting_capital,
                           backtest_starting_capital, impact=0.1):
    """
    Applies quadratic volumeshare slippage model to daily returns based
    on the proportion of the observed historical daily bar dollar volume
    consumed by the strategy's trades. Scales the size of trades based
    on the ratio of the starting capital we wish to test to the starting
    capital of the passed backtest data.

    Parameters
    ----------
    returns : pd.Series
        Time series of daily returns.
    txn_daily : pd.Series
        Daily transaciton totals, closing price, and daily volume for
        each traded name. See price_volume_daily_txns for more details.
    simulate_starting_capital : integer
        capital at which we want to test
    backtest_starting_capital: capital base at which backtest was
        origionally run. impact: See Zipline volumeshare slippage model
    impact : float
        Scales the size of the slippage penalty.

    Returns
    -------
    adj_returns : pd.Series
        Slippage penalty adjusted daily returns.
    """

    mult = simulate_starting_capital / backtest_starting_capital
    simulate_traded_shares = abs(mult * txn_daily.amount)
    simulate_traded_dollars = txn_daily.price * simulate_traded_shares
    simulate_pct_volume_used = simulate_traded_shares / txn_daily.volume

    penalties = simulate_pct_volume_used**2 \
        * impact * simulate_traded_dollars

    daily_penalty = penalties.resample('D').sum()
    daily_penalty = daily_penalty.reindex(returns.index).fillna(0)

    # Since we are scaling the numerator of the penalties linearly
    # by capital base, it makes the most sense to scale the denominator
    # similarly. In other words, since we aren't applying compounding to
    # simulate_traded_shares, we shouldn't apply compounding to pv.
    portfolio_value = ep.cum_returns(
        returns, starting_value=backtest_starting_capital) * mult

    adj_returns = returns - (daily_penalty / portfolio_value)

    return adj_returns