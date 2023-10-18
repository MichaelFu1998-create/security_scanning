def priceDF(symbol, token='', version=''):
    '''Price of ticker

    https://iexcloud.io/docs/api/#price
    4:30am-8pm ET Mon-Fri

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.io.json.json_normalize({'price': price(symbol, token, version)})
    _toDatetime(df)
    return df