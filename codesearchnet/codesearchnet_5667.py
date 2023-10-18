def tradesDF(symbol=None, token='', version=''):
    '''Trade report messages are sent when an order on the IEX Order Book is executed in whole or in part. DEEP sends a Trade report message for every individual fill.

    https://iexcloud.io/docs/api/#deep-trades

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    x = trades(symbol, token, version)
    data = []
    for key in x:
        dat = x[key]
        for d in dat:
            d['symbol'] = key
            data.append(d)
    df = pd.DataFrame(data)
    _toDatetime(df)
    return df