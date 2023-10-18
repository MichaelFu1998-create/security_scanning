def recordsDF(token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-records

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(records(token, version))
    _toDatetime(df)
    return df