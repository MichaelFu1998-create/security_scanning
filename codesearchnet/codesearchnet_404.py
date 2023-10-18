def perf_attrib(returns,
                positions,
                factor_returns,
                factor_loadings,
                transactions=None,
                pos_in_dollars=True):
    """
    Attributes the performance of a returns stream to a set of risk factors.

    Preprocesses inputs, and then calls empyrical.perf_attrib. See
    empyrical.perf_attrib for more info.

    Performance attribution determines how much each risk factor, e.g.,
    momentum, the technology sector, etc., contributed to total returns, as
    well as the daily exposure to each of the risk factors. The returns that
    can be attributed to one of the given risk factors are the
    `common_returns`, and the returns that _cannot_ be attributed to a risk
    factor are the `specific_returns`, or the alpha. The common_returns and
    specific_returns summed together will always equal the total returns.

    Parameters
    ----------
    returns : pd.Series
        Returns for each day in the date range.
        - Example:
            2017-01-01   -0.017098
            2017-01-02    0.002683
            2017-01-03   -0.008669

    positions: pd.DataFrame
        Daily holdings (in dollars or percentages), indexed by date.
        Will be converted to percentages if positions are in dollars.
        Short positions show up as cash in the 'cash' column.
        - Examples:
                        AAPL  TLT  XOM  cash
            2017-01-01    34   58   10     0
            2017-01-02    22   77   18     0
            2017-01-03   -15   27   30    15

                            AAPL       TLT       XOM  cash
            2017-01-01  0.333333  0.568627  0.098039   0.0
            2017-01-02  0.188034  0.658120  0.153846   0.0
            2017-01-03  0.208333  0.375000  0.416667   0.0

    factor_returns : pd.DataFrame
        Returns by factor, with date as index and factors as columns
        - Example:
                        momentum  reversal
            2017-01-01  0.002779 -0.005453
            2017-01-02  0.001096  0.010290

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


    transactions : pd.DataFrame, optional
        Executed trade volumes and fill prices. Used to check the turnover of
        the algorithm. Default is None, in which case the turnover check is
        skipped.

        - One row per trade.
        - Trades on different names that occur at the
          same time will have identical indicies.
        - Example:
            index                  amount   price    symbol
            2004-01-09 12:18:01    483      324.12   'AAPL'
            2004-01-09 12:18:01    122      83.10    'MSFT'
            2004-01-13 14:12:23    -75      340.43   'AAPL'

    pos_in_dollars : bool
        Flag indicating whether `positions` are in dollars or percentages
        If True, positions are in dollars.

    Returns
    -------
    tuple of (risk_exposures_portfolio, perf_attribution)

    risk_exposures_portfolio : pd.DataFrame
        df indexed by datetime, with factors as columns
        - Example:
                        momentum  reversal
            dt
            2017-01-01 -0.238655  0.077123
            2017-01-02  0.821872  1.520515

    perf_attribution : pd.DataFrame
        df with factors, common returns, and specific returns as columns,
        and datetimes as index
        - Example:
                        momentum  reversal  common_returns  specific_returns
            dt
            2017-01-01  0.249087  0.935925        1.185012          1.185012
            2017-01-02 -0.003194 -0.400786       -0.403980         -0.403980
    """
    (returns,
     positions,
     factor_returns,
     factor_loadings) = _align_and_warn(returns,
                                        positions,
                                        factor_returns,
                                        factor_loadings,
                                        transactions=transactions,
                                        pos_in_dollars=pos_in_dollars)

    # Note that we convert positions to percentages *after* the checks
    # above, since get_turnover() expects positions in dollars.
    positions = _stack_positions(positions, pos_in_dollars=pos_in_dollars)

    return ep.perf_attrib(returns, positions, factor_returns, factor_loadings)