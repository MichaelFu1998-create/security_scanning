def summaryDF(date=None, token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-historical-summary

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(summary(date, token, version))
    _toDatetime(df)
    return df