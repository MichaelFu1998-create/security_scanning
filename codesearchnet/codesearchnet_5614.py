def deepSSE(symbols=None, channels=None, on_data=None, token='', version=''):
    '''DEEP is used to receive real-time depth of book quotations direct from IEX.
    The depth of book quotations received via DEEP provide an aggregated size of resting displayed orders at a price and side,
    and do not indicate the size or number of individual orders at any price level.
    Non-displayed orders and non-displayed portions of reserve orders are not represented in DEEP.

    DEEP also provides last trade price and size information. Trades resulting from either displayed or non-displayed orders matching on IEX will be reported. Routed executions will not be reported.

    https://iexcloud.io/docs/api/#deep

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    symbols = _strCommaSeparatedString(symbols)

    channels = channels or []
    if isinstance(channels, str):
        if channels not in DeepChannelsSSE.options():
            raise PyEXception('Channel not recognized: %s', type(channels))
        channels = [channels]
    elif isinstance(channels, DeepChannelsSSE):
        channels = [channels.value]
    elif isinstance(channels, list):
        for i, c in enumerate(channels):
            if isinstance(c, DeepChannelsSSE):
                channels[i] = c.value
            elif not isinstance(c, str) or isinstance(c, str) and c not in DeepChannelsSSE.options():
                raise PyEXception('Channel not recognized: %s', c)

    channels = _strCommaSeparatedString(channels)
    return _streamSSE(_SSE_DEEP_URL_PREFIX.format(symbols=symbols, channels=channels, token=token, version=version), on_data)