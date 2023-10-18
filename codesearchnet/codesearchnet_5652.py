def deepDF(symbol=None, token='', version=''):
    '''DEEP is used to receive real-time depth of book quotations direct from IEX.
    The depth of book quotations received via DEEP provide an aggregated size of resting displayed orders at a price and side,
    and do not indicate the size or number of individual orders at any price level.
    Non-displayed orders and non-displayed portions of reserve orders are not represented in DEEP.

    DEEP also provides last trade price and size information. Trades resulting from either displayed or non-displayed orders matching on IEX will be reported. Routed executions will not be reported.

    https://iexcloud.io/docs/api/#deep

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.io.json.json_normalize(deep(symbol, token, version))
    _toDatetime(df)
    return df