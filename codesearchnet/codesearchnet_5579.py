def logoNotebook(symbol, token='', version=''):
    '''This is a helper function, but the google APIs url is standardized.

    https://iexcloud.io/docs/api/#logo
    8am UTC daily

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        image: result
    '''
    _raiseIfNotStr(symbol)
    url = logo(symbol, token, version)['url']
    return ImageI(url=url)