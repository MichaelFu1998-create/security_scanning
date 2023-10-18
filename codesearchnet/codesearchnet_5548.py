def _companyToDF(c, token='', version=''):
    '''internal'''
    df = pd.io.json.json_normalize(c)
    _toDatetime(df)
    _reindex(df, 'symbol')
    return df