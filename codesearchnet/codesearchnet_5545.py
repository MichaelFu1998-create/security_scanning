def collections(tag, collectionName, token='', version=''):
    '''Returns an array of quote objects for a given collection type. Currently supported collection types are sector, tag, and list


    https://iexcloud.io/docs/api/#collections

    Args:
        tag (string);  Sector, Tag, or List
        collectionName (string);  Associated name for tag
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    if tag not in _COLLECTION_TAGS:
        raise PyEXception('Tag must be in %s' % str(_COLLECTION_TAGS))
    return _getJson('stock/market/collection/' + tag + '?collectionName=' + collectionName, token, version)