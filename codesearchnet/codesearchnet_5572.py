def keyStatsDF(symbol, token='', version=''):
    '''Key Stats about company

    https://iexcloud.io/docs/api/#key-stats
    8am, 9am ET

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    s = keyStats(symbol, token, version)
    df = _statsToDF(s)
    return df