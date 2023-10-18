def reverse_dummies(self, X, mapping):
        """
        Convert dummy variable into numerical variables

        Parameters
        ----------
        X : DataFrame
        mapping: list-like
              Contains mappings of column to be transformed to it's new columns and value represented

        Returns
        -------
        numerical: DataFrame

        """
        out_cols = X.columns.values.tolist()
        mapped_columns = []
        for switch in mapping:
            col = switch.get('col')
            mod = switch.get('mapping')
            insert_at = out_cols.index(mod.columns[0])

            X.insert(insert_at, col, 0)
            positive_indexes = mod.index[mod.index > 0]
            for i in range(positive_indexes.shape[0]):
                existing_col = mod.columns[i]
                val = positive_indexes[i]
                X.loc[X[existing_col] == 1, col] = val
                mapped_columns.append(existing_col)
            X.drop(mod.columns, axis=1, inplace=True)
            out_cols = X.columns.values.tolist()

        return X