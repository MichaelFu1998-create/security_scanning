def difference_of_pandas_dfs(df_self, df_other, col_names=None):
    """
    Returns a dataframe with all of df_other that are not in df_self, when considering the columns specified in col_names
    :param df_self: pandas Dataframe
    :param df_other: pandas Dataframe
    :param col_names: list of column names
    :return:
    """
    df = pd.concat([df_self, df_other])
    df = df.reset_index(drop=True)
    df_gpby = df.groupby(col_names)
    idx = [x[0] for x in list(df_gpby.groups.values()) if len(x) == 1]
    df_sym_diff = df.reindex(idx)
    df_diff = pd.concat([df_other, df_sym_diff])
    df_diff = df_diff.reset_index(drop=True)
    df_gpby = df_diff.groupby(col_names)
    idx = [x[0] for x in list(df_gpby.groups.values()) if len(x) == 2]
    df_diff = df_diff.reindex(idx)
    return df_diff