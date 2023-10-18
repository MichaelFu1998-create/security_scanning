def estimatesDF(symbol, token='', version=''):
    '''Provides the latest consensus estimate for the next fiscal period

    https://iexcloud.io/docs/api/#estimates
    Updates at 9am, 11am, 12pm UTC every day

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    f = estimates(symbol, token, version)
    df = _estimatesToDF(f)
    return df