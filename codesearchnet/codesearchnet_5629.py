def recentDF(token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-recent

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(recent(token, version))
    _toDatetime(df)
    _reindex(df, 'date')
    return df