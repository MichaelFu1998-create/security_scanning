def topsWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#tops'''
    symbols = _strToList(symbols)
    if symbols:
        sendinit = ('subscribe', ','.join(symbols))
        return _stream(_wsURL('tops'), sendinit, on_data)
    return _stream(_wsURL('tops'), on_data=on_data)