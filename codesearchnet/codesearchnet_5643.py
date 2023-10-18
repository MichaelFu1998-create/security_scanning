def securityEventWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#security-event'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['securityevent']},)
    return _stream(_wsURL('deep'), sendinit, on_data)