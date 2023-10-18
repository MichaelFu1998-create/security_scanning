def companyDF(symbol, token='', version=''):
    '''Company reference data

    https://iexcloud.io/docs/api/#company
    Updates at 4am and 5am UTC every day

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    c = company(symbol, token, version)
    df = _companyToDF(c)
    return df