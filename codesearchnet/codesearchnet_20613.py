def _fill_missing_values(df, range_values, fill_value=0, fill_method=None):
        """
        Will get the names of the index colums of df, obtain their ranges from
        range_values dict and return a reindexed version of df with the given
        range values.

        :param df: pandas DataFrame

        :param range_values: dict or array-like
        Must contain for each index column of df an entry with all the values
        within the range of the column.

        :param fill_value: scalar or 'nearest', default 0
        Value to use for missing values. Defaults to 0, but can be any
        "compatible" value, e.g., NaN.
        The 'nearest' mode will fill the missing value with the nearest value in
         the column.

        :param fill_method:  {'backfill', 'bfill', 'pad', 'ffill', None}, default None
        Method to use for filling holes in reindexed DataFrame
        'pad' / 'ffill': propagate last valid observation forward to next valid
        'backfill' / 'bfill': use NEXT valid observation to fill gap

        :return: pandas Dataframe and used column ranges
        reindexed DataFrame and dict with index column ranges
        """
        idx_colnames  = df.index.names

        idx_colranges = [range_values[x] for x in idx_colnames]

        fullindex = pd.Index([p for p in product(*idx_colranges)],
                             name=tuple(idx_colnames))

        fulldf = df.reindex(index=fullindex, fill_value=fill_value,
                            method=fill_method)

        fulldf.index.names = idx_colnames

        return fulldf, idx_colranges