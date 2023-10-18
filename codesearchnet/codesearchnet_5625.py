def cryptoDF(token='', version=''):
    '''This will return an array of quotes for all Cryptocurrencies supported by the IEX API. Each element is a standard quote object with four additional keys.

    https://iexcloud.io/docs/api/#crypto

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.DataFrame(crypto(token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df