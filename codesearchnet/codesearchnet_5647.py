def tops(symbols=None, token='', version=''):
    '''TOPS provides IEX’s aggregated best quoted bid and offer position in near real time for all securities on IEX’s displayed limit order book.
    TOPS is ideal for developers needing both quote and trade data.

    https://iexcloud.io/docs/api/#tops

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    symbols = _strToList(symbols)
    if symbols:
        return _getJson('tops?symbols=' + ','.join(symbols) + '%2b', token, version)
    return _getJson('tops', token, version)