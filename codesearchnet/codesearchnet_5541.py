def _chartToDF(c):
    '''internal'''
    df = pd.DataFrame(c)
    _toDatetime(df)
    _reindex(df, 'date')
    return df