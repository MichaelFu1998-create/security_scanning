def statsDF(token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-intraday

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(stats(token, version))
    _toDatetime(df)
    return df