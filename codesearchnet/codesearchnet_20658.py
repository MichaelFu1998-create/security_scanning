def duplicated_rows(df, col_name):
    """ Return a DataFrame with the duplicated values of the column `col_name`
    in `df`."""
    _check_cols(df, [col_name])

    dups = df[pd.notnull(df[col_name]) & df.duplicated(subset=[col_name])]
    return dups