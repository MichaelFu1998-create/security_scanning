def peersDF(symbol, token='', version=''):
    '''Peers of ticker

    https://iexcloud.io/docs/api/#peers
    8am UTC daily

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    p = peers(symbol, token, version)
    df = _peersToDF(p)
    return df