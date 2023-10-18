def tradeBreakDF(symbol=None, token='', version=''):
    '''Trade break messages are sent when an execution on IEX is broken on that same trading day. Trade breaks are rare and only affect applications that rely upon IEX execution based data.

    https://iexcloud.io/docs/api/#deep-trade-break


    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.io.json.json_normalize(tradeBreak(symbol, token, version))
    _toDatetime(df)
    return df