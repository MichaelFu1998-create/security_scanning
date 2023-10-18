def histDF(date=None, token='', version=''):
    '''https://iextrading.com/developer/docs/#hist'''
    x = hist(date, token, version)
    data = []
    for key in x:
        dat = x[key]
        for item in dat:
            item['date'] = key
            data.append(item)
    df = pd.DataFrame(data)
    _toDatetime(df)
    _reindex(df, 'date')
    return df