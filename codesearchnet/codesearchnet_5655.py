def book(symbol=None, token='', version=''):
    '''Book shows IEX’s bids and asks for given symbols.

    https://iexcloud.io/docs/api/#deep-book

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(symbol)
    if symbol:
        return _getJson('deep/book?symbols=' + symbol, token, version)
    return _getJson('deep/book', token, version)