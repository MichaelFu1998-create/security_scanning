def dividendsDF(symbol, timeframe='ytd', token='', version=''):
    '''Dividend history

    https://iexcloud.io/docs/api/#dividends
    Updated at 9am UTC every day

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    d = dividends(symbol, timeframe, token, version)
    df = _dividendsToDF(d)
    return df