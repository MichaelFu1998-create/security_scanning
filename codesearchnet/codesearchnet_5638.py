def bookWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#book51'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['book']},)
    return _stream(_wsURL('deep'), sendinit, on_data)