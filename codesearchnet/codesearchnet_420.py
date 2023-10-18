def check_intraday(estimate, returns, positions, transactions):
    """
    Logic for checking if a strategy is intraday and processing it.

    Parameters
    ----------
    estimate: boolean or str, optional
        Approximate returns for intraday strategies.
        See description in tears.create_full_tear_sheet.
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.

    Returns
    -------
    pd.DataFrame
        Daily net position values, adjusted for intraday movement.
    """

    if estimate == 'infer':
        if positions is not None and transactions is not None:
            if detect_intraday(positions, transactions):
                warnings.warn('Detected intraday strategy; inferring positi' +
                              'ons from transactions. Set estimate_intraday' +
                              '=False to disable.')
                return estimate_intraday(returns, positions, transactions)
            else:
                return positions
        else:
            return positions

    elif estimate:
        if positions is not None and transactions is not None:
            return estimate_intraday(returns, positions, transactions)
        else:
            raise ValueError('Positions and txns needed to estimate intraday')
    else:
        return positions