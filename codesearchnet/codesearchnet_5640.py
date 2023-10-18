def tradingStatusWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#trading-status'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['tradingstatus']},)
    return _stream(_wsURL('deep'), sendinit, on_data)