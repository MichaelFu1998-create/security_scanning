def splitsDF(symbol, timeframe='ytd', token='', version=''):
    '''Stock split history

    https://iexcloud.io/docs/api/#splits
    Updated at 9am UTC every day

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    s = splits(symbol, timeframe, token, version)
    df = _splitsToDF(s)
    return df