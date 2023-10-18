def lastSSE(symbols=None, on_data=None, token='', version=''):
    '''Last provides trade data for executions on IEX. It is a near real time, intraday API that provides IEX last sale price, size and time.
    Last is ideal for developers that need a lightweight stock quote.

    https://iexcloud.io/docs/api/#last

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('last', symbols, on_data, token, version)