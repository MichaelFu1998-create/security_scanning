def inverse_transform(self, X_in):
        """
        Perform the inverse transformation to encoded data. Will attempt best case reconstruction, which means
        it will return nan for handle_missing and handle_unknown settings that break the bijection. We issue
        warnings when some of those cases occur.

        Parameters
        ----------
        X_in : array-like, shape = [n_samples, n_features]

        Returns
        -------
        p: array, the same size of X_in

        """
        X = X_in.copy(deep=True)

        # first check the type
        X = util.convert_input(X)

        if self._dim is None:
            raise ValueError(
                'Must train encoder before it can be used to inverse_transform data')

        # then make sure that it is the right size
        if X.shape[1] != self._dim:
            if self.drop_invariant:
                raise ValueError("Unexpected input dimension %d, the attribute drop_invariant should "
                                 "set as False when transform data" % (X.shape[1],))
            else:
                raise ValueError('Unexpected input dimension %d, expected %d' % (X.shape[1], self._dim,))

        if not self.cols:
            return X if self.return_df else X.values

        if self.handle_unknown == 'value':
            for col in self.cols:
                if any(X[col] == -1):
                    warnings.warn("inverse_transform is not supported because transform impute "
                                  "the unknown category -1 when encode %s" % (col,))

        if self.handle_unknown == 'return_nan' and self.handle_missing == 'return_nan':
            for col in self.cols:
                if X[col].isnull().any():
                    warnings.warn("inverse_transform is not supported because transform impute "
                                  "the unknown category nan when encode %s" % (col,))

        for switch in self.mapping:
            column_mapping = switch.get('mapping')
            inverse = pd.Series(data=column_mapping.index, index=column_mapping.get_values())
            X[switch.get('col')] = X[switch.get('col')].map(inverse).astype(switch.get('data_type'))

        return X if self.return_df else X.values