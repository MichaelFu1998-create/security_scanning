def transform_leave_one_out(self, X_in, y, mapping=None):
        """
        Leave one out encoding uses a single column of floats to represent the means of the target variables.
        """

        X = X_in.copy(deep=True)
        random_state_ = check_random_state(self.random_state)

        for col, colmap in mapping.items():
            level_notunique = colmap['count'] > 1

            unique_train = colmap.index
            unseen_values = pd.Series([x for x in X[col].unique() if x not in unique_train])

            is_nan = X[col].isnull()
            is_unknown_value = X[col].isin(unseen_values.dropna())

            if self.handle_unknown == 'error' and is_unknown_value.any():
                raise ValueError('Columns to be encoded can not contain new values')

            if y is None:    # Replace level with its mean target; if level occurs only once, use global mean
                level_means = (colmap['sum'] / colmap['count']).where(level_notunique, self._mean)
                X[col] = X[col].map(level_means)
            else:            # Replace level with its mean target, calculated excluding this row's target
                # The y (target) mean for this level is normally just the sum/count;
                # excluding this row's y, it's (sum - y) / (count - 1)
                level_means = (X[col].map(colmap['sum']) - y) / (X[col].map(colmap['count']) - 1)
                # The 'where' fills in singleton levels (count = 1 -> div by 0) with the global mean
                X[col] = level_means.where(X[col].map(colmap['count'][level_notunique]).notnull(), self._mean)

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