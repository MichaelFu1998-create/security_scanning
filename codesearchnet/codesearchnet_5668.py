def tradeBreak(symbol=None, token='', version=''):
    '''Trade break messages are sent when an execution on IEX is broken on that same trading day. Trade breaks are rare and only affect applications that rely upon IEX execution based data.

    https://iexcloud.io/docs/api/#deep-trade-break


    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(symbol)
    if symbol:
        return _getJson('deep/trade-breaks?symbols=' + symbol, token, version)
    return _getJson('deep/trade-breaks', token, version)