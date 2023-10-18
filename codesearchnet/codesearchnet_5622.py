def systemEventSSE(symbols=None, on_data=None, token='', version=''):
    '''The System event message is used to indicate events that apply to the market or the data feed.

    There will be a single message disseminated per channel for each System Event type within a given trading session.

    https://iexcloud.io/docs/api/#deep-system-event

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('system-event', symbols, on_data, token, version)