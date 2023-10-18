def listDF(option='mostactive', token='', version=''):
    '''Returns an array of quotes for the top 10 symbols in a specified list.


    https://iexcloud.io/docs/api/#list
    Updated intraday

    Args:
        option (string); Option to query
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(list(option, token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df