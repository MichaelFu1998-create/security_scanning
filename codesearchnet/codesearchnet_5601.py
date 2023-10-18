def sectorPerformanceDF(token='', version=''):
    '''This returns an array of each sector and performance for the current trading day. Performance is based on each sector ETF.

    https://iexcloud.io/docs/api/#sector-performance
    8am-5pm ET Mon-Fri

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(sectorPerformance(token, version))
    _toDatetime(df)
    _reindex(df, 'name')
    return df