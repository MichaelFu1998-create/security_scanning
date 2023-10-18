def put_df_as_ndarray(self, key, df, range_values, loop_multiindex=False,
                          unstack=False, fill_value=0, fill_method=None):
        """Returns a PyTables HDF Array from df in the shape given by its index columns range values.

        :param key: string object

        :param df: pandas DataFrame

        :param range_values: dict or array-like
        Must contain for each index column of df an entry with all the values
        within the range of the column.

        :param loop_multiindex: bool
        Will loop through the first index in a multiindex dataframe, extract a
        dataframe only for one value, complete and fill the missing values and
        store in the HDF.
        If this is True, it will not use unstack.
        This is as fast as unstacking.

        :param unstack: bool
        Unstack means that this will use the first index name to
        unfold the DataFrame, and will create a group with as many datasets
        as valus has this first index.
        Use this if you think the filled dataframe won't fit in your RAM memory.
        If set to False, this will transform the dataframe in memory first
        and only then save it.

        :param fill_value: scalar or 'nearest', default 0
        Value to use for missing values. Defaults to 0, but can be any
        "compatible" value, e.g., NaN.
        The 'nearest' mode will fill the missing value with the nearest value in
         the column.

        :param fill_method:  {'backfill', 'bfill', 'pad', 'ffill', None}, default None
        Method to use for filling holes in reindexed DataFrame
        'pad' / 'ffill': propagate last valid observation forward to next valid
        'backfill' / 'bfill': use NEXT valid observation to fill gap

        :return: PyTables data node
        """
        idx_colnames = df.index.names
        #idx_colranges = [range_values[x] for x in idx_colnames]

        #dataset group name if not given
        if key is None:
            key = idx_colnames[0]

        if loop_multiindex:
            idx_values = df.index.get_level_values(0).unique()

            for idx in idx_values:
                vals, _ = self._fill_missing_values(df.xs((idx,), level=idx_colnames[0]),
                                                    range_values,
                                                    fill_value=fill_value,
                                                    fill_method=fill_method)

                ds_name = str(idx) + '_' + '_'.join(vals.columns)

                self._push_dfblock(key, vals, ds_name, range_values)

            return self._handle.get_node('/' + str(key))

        #separate the dataframe into blocks, only with the first index
        else:
            if unstack:
                df = df.unstack(idx_colnames[0])
                for idx in df:
                    vals, _ = self._fill_missing_values(df[idx], range_values,
                                                        fill_value=fill_value,
                                                        fill_method=fill_method)
                    vals = np.nan_to_num(vals)

                    ds_name = '_'.join([str(x) for x in vals.name])

                    self._push_dfblock(key, vals, ds_name, range_values)

                return self._handle.get_node('/' + str(key))

        #not separate the data
        vals, _ = self._fill_missing_values(df, range_values,
                                            fill_value=fill_value,
                                            fill_method=fill_method)

        ds_name = self._array_dsname

        return self._push_dfblock(key, vals, ds_name, range_values)