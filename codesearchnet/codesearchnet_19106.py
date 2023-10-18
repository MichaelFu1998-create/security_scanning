def inverse_transform(self, X, **params):
        '''
        Transform data back to its original space, i.e., return an input
        X_original whose transform would (maybe approximately) be X.

        Parameters
        ----------
        X : :class:`Features` or list of bag feature arrays
            Data to train on and transform.

        any other keyword argument :
            Passed on as keyword arguments to the transformer's 
            ``inverse_transform()``.

        Returns
        -------
        X_original : :class:`Features`
        '''
        X = as_features(X, stack=True)
        Xo = self.transformer.inverse_transform(X.stacked_features, **params)
        return self._gather_outputs(X, Xo)