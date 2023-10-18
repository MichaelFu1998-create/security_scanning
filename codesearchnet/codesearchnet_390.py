def get_max_days_to_liquidate_by_ticker(positions, market_data,
                                        max_bar_consumption=0.2,
                                        capital_base=1e6,
                                        mean_volume_window=5,
                                        last_n_days=None):
    """
    Finds the longest estimated liquidation time for each traded
    name over the course of backtest (or last n days of the backtest).

    Parameters
    ----------
    positions: pd.DataFrame
        Contains daily position values including cash
        - See full explanation in tears.create_full_tear_sheet
    market_data : pd.Panel
        Panel with items axis of 'price' and 'volume' DataFrames.
        The major and minor axes should match those of the
        the passed positions DataFrame (same dates and symbols).
    max_bar_consumption : float
        Max proportion of a daily bar that can be consumed in the
        process of liquidating a position.
    capital_base : integer
        Capital base multiplied by portfolio allocation to compute
        position value that needs liquidating.
    mean_volume_window : float
        Trailing window to use in mean volume calculation.
    last_n_days : integer
        Compute for only the last n days of the passed backtest data.

    Returns
    -------
    days_to_liquidate : pd.DataFrame
        Max Number of days required to fully liquidate each traded name.
        Index of symbols. Columns for days_to_liquidate and the corresponding
        date and position_alloc on that day.
    """

    dtlp = days_to_liquidate_positions(positions, market_data,
                                       max_bar_consumption=max_bar_consumption,
                                       capital_base=capital_base,
                                       mean_volume_window=mean_volume_window)

    if last_n_days is not None:
        dtlp = dtlp.loc[dtlp.index.max() - pd.Timedelta(days=last_n_days):]

    pos_alloc = pos.get_percent_alloc(positions)
    pos_alloc = pos_alloc.drop('cash', axis=1)

    liq_desc = pd.DataFrame()
    liq_desc['days_to_liquidate'] = dtlp.unstack()
    liq_desc['pos_alloc_pct'] = pos_alloc.unstack() * 100
    liq_desc.index.levels[0].name = 'symbol'
    liq_desc.index.levels[1].name = 'date'

    worst_liq = liq_desc.reset_index().sort_values(
        'days_to_liquidate', ascending=False).groupby('symbol').first()

    return worst_liq