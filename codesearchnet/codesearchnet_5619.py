def officialPriceSSE(symbols=None, on_data=None, token='', version=''):
    '''The Official Price message is used to disseminate the IEX Official Opening and Closing Prices.

    These messages will be provided only for IEX Listed Securities.

    https://iexcloud.io/docs/api/#deep-official-price

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('official-price', symbols, on_data, token, version)