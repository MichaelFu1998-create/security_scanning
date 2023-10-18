def sentimentDF(symbol, type='daily', date=None, token='', version=''):
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
        DataFrame: result
    '''
    ret = sentiment(symbol, type, date, token, version)
    if type == 'daiy':
        ret = [ret]
    df = pd.DataFrame(ret)
    _toDatetime(df)
    return df