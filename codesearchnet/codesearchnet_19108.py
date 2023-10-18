def transform(self, X):
        """Scaling features of X according to feature_range.

        Parameters
        ----------
        X : array-like with shape [n_samples, n_features]
            Input data that will be transformed.
        """
        X = check_array(X, copy=self.copy)
        X *= self.scale_
        X += self.min_
        if self.truncate:
            np.maximum(self.feature_range[0], X, out=X)
            np.minimum(self.feature_range[1], X, out=X)
        return X