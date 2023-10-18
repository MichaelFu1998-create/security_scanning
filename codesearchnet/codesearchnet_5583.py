def marketNewsDF(count=10, token='', version=''):
    '''News about market

    https://iexcloud.io/docs/api/#news
    Continuous

    Args:
        count (int): limit number of results
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(marketNews(count, token, version))
    _toDatetime(df)
    _reindex(df, 'datetime')
    return df