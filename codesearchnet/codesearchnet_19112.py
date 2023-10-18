def fit_transform(self, X):
        '''
        Compute clustering and transform a list of bag features into its
        bag-of-words representation. Like calling fit(X) and then transform(X),
        but more efficient.

        Parameters
        ----------
        X : :class:`skl_groups.features.Features` or list of bag feature arrays
            New data to transform.

        Returns
        -------
        X_new : integer array, shape [len(X), kmeans.n_clusters]
            X transformed into the new space.
        '''
        X = as_features(X, stack=True)
        self.kmeans_fit_ = copy(self.kmeans)
        assignments = self.kmeans_fit_.fit_predict(X.stacked_features) 
        return self._group_assignments(X, assignments)