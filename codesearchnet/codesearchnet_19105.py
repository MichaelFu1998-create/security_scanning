def fit_transform(self, X, y=None, **params):
        '''
        Fit and transform the stacked points.

        Parameters
        ----------
        X : :class:`Features` or list of bag feature arrays
            Data to train on and transform.

        any other keyword argument :
            Passed on as keyword arguments to the transformer's ``transform()``.

        Returns
        -------
        X_new : :class:`Features`
            Transformed features.
        '''
        X = as_features(X, stack=True)
        X_new = self.transformer.fit_transform(X.stacked_features, y, **params)
        return self._gather_outputs(X, X_new)