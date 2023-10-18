def sentiment(symbol, type='daily', date=None, token='', version=''):
    '''This endpoint provides social sentiment data from StockTwits. Data can be viewed as a daily value, or by minute for a given date.

    https://iexcloud.io/docs/api/#social-sentiment
    Continuous

    Args:
        symbol (string); Ticker to request
        type (string); 'daily' or 'minute'
        date (string); date in YYYYMMDD or datetime
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(symbol)
    if date:
        date = _strOrDate(date)
        return _getJson('stock/{symbol}/sentiment/{type}/{date}'.format(symbol=symbol, type=type, date=date), token, version)
    return _getJson('stock/{symbol}/sentiment/{type}/'.format(symbol=symbol, type=type), token, version)