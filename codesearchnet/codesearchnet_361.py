def extract_pos(positions, cash):
    """
    Extract position values from backtest object as returned by
    get_backtest() on the Quantopian research platform.

    Parameters
    ----------
    positions : pd.DataFrame
        timeseries containing one row per symbol (and potentially
        duplicate datetime indices) and columns for amount and
        last_sale_price.
    cash : pd.Series
        timeseries containing cash in the portfolio.

    Returns
    -------
    pd.DataFrame
        Daily net position values.
         - See full explanation in tears.create_full_tear_sheet.
    """

    positions = positions.copy()
    positions['values'] = positions.amount * positions.last_sale_price

    cash.name = 'cash'

    values = positions.reset_index().pivot_table(index='index',
                                                 columns='sid',
                                                 values='values')

    if ZIPLINE:
        for asset in values.columns:
            if type(asset) in [Equity, Future]:
                values[asset] = values[asset] * asset.price_multiplier

    values = values.join(cash).fillna(0)

    # NOTE: Set name of DataFrame.columns to sid, to match the behavior
    # of DataFrame.join in earlier versions of pandas.
    values.columns.name = 'sid'

    return values