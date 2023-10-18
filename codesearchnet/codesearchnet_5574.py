def largestTradesDF(symbol, token='', version=''):
    '''This returns 15 minute delayed, last sale eligible trades.

    https://iexcloud.io/docs/api/#largest-trades
    9:30-4pm ET M-F during regular market hours

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(largestTrades(symbol, token, version))
    _toDatetime(df)
    _reindex(df, 'time')
    return df