def transform(self, X, **params):
        '''
        Transform the stacked points.

        Parameters
        ----------
        X : :class:`Features` or list of bag feature arrays
            New data to transform.

        any other keyword argument :
            Passed on as keyword arguments to the transformer's ``transform()``.

        Returns
        -------
        X_new : :class:`Features`
            Transformed features.
        '''
        X = as_features(X, stack=True)
        X_new = self.transformer.transform(X.stacked_features, **params)
        return self._gather_outputs(X, X_new)