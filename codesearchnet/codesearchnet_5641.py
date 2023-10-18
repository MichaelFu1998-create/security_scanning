def opHaltStatusWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#operational-halt-status'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['ophaltstatus']},)
    return _stream(_wsURL('deep'), sendinit, on_data)