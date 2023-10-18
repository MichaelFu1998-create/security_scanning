def tradesSSE(symbols=None, on_data=None, token='', version=''):
    '''Trade report messages are sent when an order on the IEX Order Book is executed in whole or in part. DEEP sends a Trade report message for every individual fill.

    https://iexcloud.io/docs/api/#deep-trades

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    symbols = _strCommaSeparatedString(symbols)
    return _streamSSE(_SSE_DEEP_URL_PREFIX.format(symbols=symbols, channels='trades', token=token, version=version), on_data)