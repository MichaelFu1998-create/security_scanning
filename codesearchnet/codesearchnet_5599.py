def relevant(symbol, token='', version=''):
    '''Same as peers

    https://iexcloud.io/docs/api/#relevant
    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(symbol)
    return _getJson('stock/' + symbol + '/relevant', token, version)