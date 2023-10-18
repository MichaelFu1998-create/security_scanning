def collectionsDF(tag, query, token='', version=''):
    '''Returns an array of quote objects for a given collection type. Currently supported collection types are sector, tag, and list


    https://iexcloud.io/docs/api/#collections

    Args:
        tag (string);  Sector, Tag, or List
        collectionName (string);  Associated name for tag
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(collections(tag, query, token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df