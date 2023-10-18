def _remove_I_columns(df):
    """
    Remove columns ending with I from a pandas.DataFrame

    Parameters
    ----------
    df: dataFrame

    Returns
    -------
    None
    """
    all_columns = list(filter(lambda el: el[-2:] == "_I", df.columns))
    for column in all_columns:
        del df[column]