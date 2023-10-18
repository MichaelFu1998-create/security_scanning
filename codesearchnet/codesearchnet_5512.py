def internationalSymbols(region='', exchange='', token='', version=''):
    '''This call returns an array of international symbols that IEX Cloud supports for API calls.

    https://iexcloud.io/docs/api/#international-symbols
    8am, 9am, 12pm, 1pm UTC daily

    Args:
        region (string); region, 2 letter case insensitive string of country codes using ISO 3166-1 alpha-2
        exchange (string): Case insensitive string of Exchange using IEX Supported Exchanges list
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    if region:
        return _getJson('ref-data/region/{region}/symbols'.format(region=region), token, version)
    elif exchange:
        return _getJson('ref-data/exchange/{exchange}/exchange'.format(exchange=exchange), token, version)
    return _getJson('ref-data/region/us/symbols', token, version)