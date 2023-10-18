def delayedQuoteDF(symbol, token='', version=''):
    '''This returns the 15 minute delayed market quote.

    https://iexcloud.io/docs/api/#delayed-quote
    15min delayed
    4:30am - 8pm ET M-F when market is open

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    df = pd.io.json.json_normalize(delayedQuote(symbol, token, version))
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df