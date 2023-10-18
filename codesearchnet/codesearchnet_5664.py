def ssrStatusDF(symbol=None, token='', version=''):
    '''In association with Rule 201 of Regulation SHO, the Short Sale Price Test Message is used to indicate when a short sale price test restriction is in effect for a security.

    IEX disseminates a full pre-market spin of Short sale price test status messages indicating the Rule 201 status of all securities.
     After the pre-market spin, IEX will use the Short sale price test status message in the event of an intraday status change.

    The IEX Trading System will process orders based on the latest short sale price test restriction status.

    https://iexcloud.io/docs/api/#deep-short-sale-price-test-status

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    x = ssrStatus(symbol, token, version)
    data = []
    for key in x:
        d = x[key]
        d['symbol'] = key
        data.append(d)
    df = pd.DataFrame(data)
    _toDatetime(df)
    return df