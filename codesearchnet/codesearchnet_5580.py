def news(symbol, count=10, token='', version=''):
    '''News about company

    https://iexcloud.io/docs/api/#news
    Continuous

    Args:
        symbol (string); Ticker to request
        count (int): limit number of results
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(symbol)
    return _getJson('stock/' + symbol + '/news/last/' + str(count), token, version)