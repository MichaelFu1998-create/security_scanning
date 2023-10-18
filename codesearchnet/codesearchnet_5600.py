def relevantDF(symbol, token='', version=''):
    '''Same as peers

    https://iexcloud.io/docs/api/#relevant
    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(relevant(symbol, token, version))
    _toDatetime(df)
    return df