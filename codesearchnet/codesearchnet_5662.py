def securityEventDF(symbol=None, token='', version=''):
    '''The Security event message is used to indicate events that apply to a security. A Security event message will be sent whenever such event occurs

    https://iexcloud.io/docs/api/#deep-security-event

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    x = securityEvent(symbol, token, version)
    data = []
    for key in x:
        d = x[key]
        d['symbol'] = key
        data.append(d)
    df = pd.DataFrame(data)
    _toDatetime(df)
    return df