def get_turnover(positions, transactions, denominator='AGB'):
    """
     - Value of purchases and sales divided
    by either the actual gross book or the portfolio value
    for the time step.

    Parameters
    ----------
    positions : pd.DataFrame
        Contains daily position values including cash.
        - See full explanation in tears.create_full_tear_sheet
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
        - See full explanation in tears.create_full_tear_sheet
    denominator : str, optional
        Either 'AGB' or 'portfolio_value', default AGB.
        - AGB (Actual gross book) is the gross market
        value (GMV) of the specific algo being analyzed.
        Swapping out an entire portfolio of stocks for
        another will yield 200% turnover, not 100%, since
        transactions are being made for both sides.
        - We use average of the previous and the current end-of-period
        AGB to avoid singularities when trading only into or
        out of an entire book in one trading period.
        - portfolio_value is the total value of the algo's
        positions end-of-period, including cash.

    Returns
    -------
    turnover_rate : pd.Series
        timeseries of portfolio turnover rates.
    """

    txn_vol = get_txn_vol(transactions)
    traded_value = txn_vol.txn_volume

    if denominator == 'AGB':
        # Actual gross book is the same thing as the algo's GMV
        # We want our denom to be avg(AGB previous, AGB current)
        AGB = positions.drop('cash', axis=1).abs().sum(axis=1)
        denom = AGB.rolling(2).mean()

        # Since the first value of pd.rolling returns NaN, we
        # set our "day 0" AGB to 0.
        denom.iloc[0] = AGB.iloc[0] / 2
    elif denominator == 'portfolio_value':
        denom = positions.sum(axis=1)
    else:
        raise ValueError(
            "Unexpected value for denominator '{}'. The "
            "denominator parameter must be either 'AGB'"
            " or 'portfolio_value'.".format(denominator)
        )

    denom.index = denom.index.normalize()
    turnover = traded_value.div(denom, axis='index')
    turnover = turnover.fillna(0)
    return turnover