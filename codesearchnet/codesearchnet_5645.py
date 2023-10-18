def auctionWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#auction'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['auction']},)
    return _stream(_wsURL('deep'), sendinit, on_data)