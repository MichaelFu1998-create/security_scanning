def bookSSE(symbols=None, on_data=None, token='', version=''):
    '''Book shows IEX’s bids and asks for given symbols.

    https://iexcloud.io/docs/api/#deep-book

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('book', symbols, on_data, token, version)