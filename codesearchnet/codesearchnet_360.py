def get_max_median_position_concentration(positions):
    """
    Finds the max and median long and short position concentrations
    in each time period specified by the index of positions.

    Parameters
    ----------
    positions : pd.DataFrame
        The positions that the strategy takes over time.

    Returns
    -------
    pd.DataFrame
        Columns are max long, max short, median long, and median short
        position concentrations. Rows are timeperiods.
    """

    expos = get_percent_alloc(positions)
    expos = expos.drop('cash', axis=1)

    longs = expos.where(expos.applymap(lambda x: x > 0))
    shorts = expos.where(expos.applymap(lambda x: x < 0))

    alloc_summary = pd.DataFrame()
    alloc_summary['max_long'] = longs.max(axis=1)
    alloc_summary['median_long'] = longs.median(axis=1)
    alloc_summary['median_short'] = shorts.median(axis=1)
    alloc_summary['max_short'] = shorts.min(axis=1)

    return alloc_summary