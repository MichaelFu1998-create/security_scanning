def _getJson(url, token='', version=''):
    '''for backwards compat, accepting token and version but ignoring'''
    if token:
        return _getJsonIEXCloud(url, token, version)
    return _getJsonOrig(url)