def col_values(df, col_name):
    """ Return a list of not null values from the `col_name` column of `df`."""
    _check_cols(df, [col_name])

    if 'O' in df[col_name] or pd.np.issubdtype(df[col_name].dtype, str): # if the column is of strings
        return [nom.lower() for nom in df[pd.notnull(df)][col_name] if not pd.isnull(nom)]
    else:
        return [nom for nom in df[pd.notnull(df)][col_name] if not pd.isnull(nom)]