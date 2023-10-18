def dailyDF(date=None, last='', token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-historical-daily

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(daily(date, last, token, version))
    _toDatetime(df)
    return df