def fit(self, X, y=None):
        '''
        Choose the codewords based on a training set.

        Parameters
        ----------
        X : :class:`skl_groups.features.Features` or list of arrays of shape ``[n_samples[i], n_features]``
            Training set. If a Features object, it will be stacked.
        '''
        self.kmeans_fit_ = copy(self.kmeans)
        X = as_features(X, stack=True)
        self.kmeans_fit_.fit(X.stacked_features) 
        return self