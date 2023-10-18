def tradeBreakWS(symbols=None, on_data=None):
    '''https://iextrading.com/developer/docs/#trade-break'''
    symbols = _strToList(symbols)
    sendinit = ({'symbols': symbols, 'channels': ['tradebreaks']},)
    return _stream(_wsURL('deep'), sendinit, on_data)