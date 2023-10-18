def last(symbols=None, token='', version=''):
    '''Last provides trade data for executions on IEX. It is a near real time, intraday API that provides IEX last sale price, size and time.
    Last is ideal for developers that need a lightweight stock quote.

    https://iexcloud.io/docs/api/#last

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    symbols = _strToList(symbols)
    if symbols:
        return _getJson('tops/last?symbols=' + ','.join(symbols) + '%2b', token, version)
    return _getJson('tops/last', token, version)