def ssrStatusWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#short-sale-price-test-status'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['ssr']},)
    return _stream(_wsURL('deep'), sendinit, on_data)