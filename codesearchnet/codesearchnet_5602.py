def _splitsToDF(s):
    '''internal'''
    df = pd.DataFrame(s)
    _toDatetime(df)
    _reindex(df, 'exDate')
    return df