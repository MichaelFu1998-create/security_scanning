def get_long_short_pos(positions):
    """
    Determines the long and short allocations in a portfolio.

    Parameters
    ----------
    positions : pd.DataFrame
        The positions that the strategy takes over time.

    Returns
    -------
    df_long_short : pd.DataFrame
        Long and short allocations as a decimal
        percentage of the total net liquidation
    """

    pos_wo_cash = positions.drop('cash', axis=1)
    longs = pos_wo_cash[pos_wo_cash > 0].sum(axis=1).fillna(0)
    shorts = pos_wo_cash[pos_wo_cash < 0].sum(axis=1).fillna(0)
    cash = positions.cash
    net_liquidation = longs + shorts + cash
    df_pos = pd.DataFrame({'long': longs.divide(net_liquidation, axis='index'),
                           'short': shorts.divide(net_liquidation,
                                                  axis='index')})
    df_pos['net exposure'] = df_pos['long'] + df_pos['short']
    return df_pos