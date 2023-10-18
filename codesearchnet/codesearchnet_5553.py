def _dividendsToDF(d):
    '''internal'''
    df = pd.DataFrame(d)
    _toDatetime(df)
    _reindex(df, 'exDate')
    return df