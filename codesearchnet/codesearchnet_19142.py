def transform(self, X):
        '''
        Transform a list of bag features into a matrix of its mean features.

        Parameters
        ----------
        X : :class:`skl_groups.features.Features` or list of bag feature arrays
            Data to transform.

        Returns
        -------
        X_new : array, shape ``[len(X), X.dim]``
            X transformed into its means.
        '''
        X = as_features(X)
        return np.vstack([np.mean(bag, axis=0) for bag in X])