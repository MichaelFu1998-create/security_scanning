def symbolsDF(token='', version=''):
    '''This call returns an array of symbols that IEX Cloud supports for API calls.

    https://iexcloud.io/docs/api/#symbols
    8am, 9am, 12pm, 1pm UTC daily

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        dataframe: result
    '''
    df = pd.DataFrame(symbols(token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df