def _reindex(df, col):
    '''internal'''
    if col in df.columns:
        df.set_index(col, inplace=True)