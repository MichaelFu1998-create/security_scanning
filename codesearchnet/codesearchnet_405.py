def compute_exposures(positions, factor_loadings, stack_positions=True,
                      pos_in_dollars=True):
    """
    Compute daily risk factor exposures.

    Normalizes positions (if necessary) and calls ep.compute_exposures.
    See empyrical.compute_exposures for more info.

    Parameters
    ----------
    positions: pd.DataFrame or pd.Series
        Daily holdings (in dollars or percentages), indexed by date, OR
        a series of holdings indexed by date and ticker.
        - Examples:
                        AAPL  TLT  XOM  cash
            2017-01-01    34   58   10     0
            2017-01-02    22   77   18     0
            2017-01-03   -15   27   30    15

                            AAPL       TLT       XOM  cash
            2017-01-01  0.333333  0.568627  0.098039   0.0
            2017-01-02  0.188034  0.658120  0.153846   0.0
            2017-01-03  0.208333  0.375000  0.416667   0.0

            dt          ticker
            2017-01-01  AAPL      0.417582
                        TLT       0.010989
                        XOM       0.571429
            2017-01-02  AAPL      0.202381
                        TLT       0.535714
                        XOM       0.261905

    factor_loadings : pd.DataFrame
        Factor loadings for all days in the date range, with date and ticker as
        index, and factors as columns.
        - Example:
                               momentum  reversal
            dt         ticker
            2017-01-01 AAPL   -1.592914  0.852830
                       TLT     0.184864  0.895534
                       XOM     0.993160  1.149353
            2017-01-02 AAPL   -0.140009 -0.524952
                       TLT    -1.066978  0.185435
                       XOM    -1.798401  0.761549

    stack_positions : bool
        Flag indicating whether `positions` should be converted to long format.

    pos_in_dollars : bool
        Flag indicating whether `positions` are in dollars or percentages
        If True, positions are in dollars.

    Returns
    -------
    risk_exposures_portfolio : pd.DataFrame
        df indexed by datetime, with factors as columns.
        - Example:
                        momentum  reversal
            dt
            2017-01-01 -0.238655  0.077123
            2017-01-02  0.821872  1.520515
    """
    if stack_positions:
        positions = _stack_positions(positions, pos_in_dollars=pos_in_dollars)

    return ep.compute_exposures(positions, factor_loadings)