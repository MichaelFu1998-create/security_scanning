def transform_leave_one_out(self, X_in, y, mapping=None):
        """
        Leave one out encoding uses a single column of floats to represent the means of the target variables.
        """
        X = X_in.copy(deep=True)
        random_state_ = check_random_state(self.random_state)

        # Prepare the data
        if y is not None:
            # Convert bools to numbers (the target must be summable)
            y = y.astype('double')

            # Cumsum and cumcount do not work nicely with None.
            # This is a terrible workaround that will fail, when the
            # categorical input contains -999.9
            for cat_col in X.select_dtypes('category').columns.values:
                X[cat_col] = X[cat_col].cat.add_categories(-999.9)
            X = X.fillna(-999.9)

        for col, colmap in mapping.items():
            level_notunique = colmap['count'] > 1

            unique_train = colmap.index
            unseen_values = pd.Series([x for x in X_in[col].unique() if x not in unique_train])

            is_nan = X_in[col].isnull()
            is_unknown_value = X_in[col].isin(unseen_values.dropna())

            if self.handle_unknown == 'error' and is_unknown_value.any():
                raise ValueError('Columns to be encoded can not contain new values')

            if y is None:    # Replace level with its mean target; if level occurs only once, use global mean
                level_means = ((colmap['sum'] + self._mean) / (colmap['count'] + 1)).where(level_notunique, self._mean)
                X[col] = X[col].map(level_means)
            else:
                # Simulation of CatBoost implementation, which calculates leave-one-out on the fly.
                # The nice thing about this is that it helps to prevent overfitting. The bad thing
                # is that CatBoost uses many iterations over the data. But we run just one iteration.
                # Still, it works better than leave-one-out without any noise.
                # See:
                #   https://tech.yandex.com/catboost/doc/dg/concepts/algorithm-main-stages_cat-to-numberic-docpage/
                temp = y.groupby(X[col]).agg(['cumsum', 'cumcount'])
                X[col] = (temp['cumsum'] - y + self._mean) / (temp['cumcount'] + 1)

            if self.handle_unknown == 'value':
                X.loc[is_unknown_value, col] = self._mean
            elif self.handle_unknown == 'return_nan':
                X.loc[is_unknown_value, col] = np.nan

            if self.handle_missing == 'value':
                X.loc[is_nan & unseen_values.isnull().any(), col] = self._mean
            elif self.handle_missing == 'return_nan':
                X.loc[is_nan, col] = np.nan

            if self.sigma is not None and y is not None:
                X[col] = X[col] * random_state_.normal(1., self.sigma, X[col].shape[0])

        return X