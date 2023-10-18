def officialPriceWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#official-price'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['official-price']},)
    return _stream(_wsURL('deep'), sendinit, on_data)