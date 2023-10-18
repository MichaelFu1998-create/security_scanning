def fit(self, X, y=None, **params):
        '''
        Fit the transformer on the stacked points.

        Parameters
        ----------
        X : :class:`Features` or list of arrays of shape ``[n_samples[i], n_features]``
            Training set. If a Features object, it will be stacked.

        any other keyword argument :
            Passed on as keyword arguments to the transformer's ``fit()``.
        '''
        X = as_features(X, stack=True)
        self.transformer.fit(X.stacked_features, y, **params)
        return self