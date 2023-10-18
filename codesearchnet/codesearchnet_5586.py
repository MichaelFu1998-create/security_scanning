def marketOhlcDF(token='', version=''):
    '''Returns the official open and close for whole market.

    https://iexcloud.io/docs/api/#news
    9:30am-5pm ET Mon-Fri

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    x = marketOhlc(token, version)
    data = []
    for key in x:
        data.append(x[key])
        data[-1]['symbol'] = key
    df = pd.io.json.json_normalize(data)
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df