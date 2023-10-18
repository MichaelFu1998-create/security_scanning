def days_to_liquidate_positions(positions, market_data,
                                max_bar_consumption=0.2,
                                capital_base=1e6,
                                mean_volume_window=5):
    """
    Compute the number of days that would have been required
    to fully liquidate each position on each day based on the
    trailing n day mean daily bar volume and a limit on the proportion
    of a daily bar that we are allowed to consume.

    This analysis uses portfolio allocations and a provided capital base
    rather than the dollar values in the positions DataFrame to remove the
    effect of compounding on days to liquidate. In other words, this function
    assumes that the net liquidation portfolio value will always remain
    constant at capital_base.

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

    Returns
    -------
    days_to_liquidate : pd.DataFrame
        Number of days required to fully liquidate daily positions.
        Datetime index, symbols as columns.
    """

    DV = market_data['volume'] * market_data['price']
    roll_mean_dv = DV.rolling(window=mean_volume_window,
                              center=False).mean().shift()
    roll_mean_dv = roll_mean_dv.replace(0, np.nan)

    positions_alloc = pos.get_percent_alloc(positions)
    positions_alloc = positions_alloc.drop('cash', axis=1)

    days_to_liquidate = (positions_alloc * capital_base) / \
        (max_bar_consumption * roll_mean_dv)

    return days_to_liquidate.iloc[mean_volume_window:]