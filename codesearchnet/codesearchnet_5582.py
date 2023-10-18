def newsDF(symbol, count=10, token='', version=''):
    '''News about company

    https://iexcloud.io/docs/api/#news
    Continuous

    Args:
        symbol (string); Ticker to request
        count (int): limit number of results
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    n = news(symbol, count, token, version)
    df = _newsToDF(n)
    return df