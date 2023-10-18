def mutualFundSymbolsDF(token='', version=''):
    '''This call returns an array of mutual fund symbols that IEX Cloud supports for API calls.

    https://iexcloud.io/docs/api/#mutual-fund-symbols
    8am, 9am, 12pm, 1pm UTC daily

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(mutualFundSymbols(token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df