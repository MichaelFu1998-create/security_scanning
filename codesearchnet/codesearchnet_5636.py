def lastWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#last'''
    symbols = _strToList(symbols)
    if symbols:
        sendinit = ('subscribe', ','.join(symbols))
        return _stream(_wsURL('last'), sendinit, on_data)
    return _stream(_wsURL('last'), on_data=on_data)