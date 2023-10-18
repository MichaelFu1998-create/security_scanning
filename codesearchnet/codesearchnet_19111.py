def transform(self, X):
        '''
        Transform a list of bag features into its bag-of-words representation.

        Parameters
        ----------
        X : :class:`skl_groups.features.Features` or list of bag feature arrays
            New data to transform.

        Returns
        -------
        X_new : integer array, shape [len(X), kmeans.n_clusters]
            X transformed into the new space.
        '''
        self._check_fitted()
        X = as_features(X, stack=True)
        assignments = self.kmeans_fit_.predict(X.stacked_features)
        return self._group_assignments(X, assignments)