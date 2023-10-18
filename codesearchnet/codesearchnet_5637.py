def deepWS(symbols=None, channels=None, on_data=None):
    '''https://iextrading.com/developer/docs/#deep'''
    symbols = _strToList(symbols)

    channels = channels or []
    if isinstance(channels, str):
        if channels not in DeepChannels.options():
            raise PyEXception('Channel not recognized: %s', type(channels))
        channels = [channels]
    elif isinstance(channels, DeepChannels):
        channels = [channels.value]
    elif isinstance(channels, list):
        for i, c in enumerate(channels):
            if isinstance(c, DeepChannels):
                channels[i] = c.value
            elif not isinstance(c, str) or isinstance(c, str) and c not in DeepChannels.options():
                raise PyEXception('Channel not recognized: %s', c)

    sendinit = ({'symbols': symbols, 'channels': channels},)
    return _stream(_wsURL('deep'), sendinit, on_data)