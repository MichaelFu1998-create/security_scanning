def tradesWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#trades'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['trades']},)
    return _stream(_wsURL('deep'), sendinit, on_data)