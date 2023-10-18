def _newsToDF(n):
    '''internal'''
    df = pd.DataFrame(n)
    _toDatetime(df)
    _reindex(df, 'datetime')
    return df