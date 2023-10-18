def inverse_transform(self, X):
        """Undo the scaling of X according to feature_range.

        Note that if truncate is true, any truncated points will not
        be restored exactly.

        Parameters
        ----------
        X : array-like with shape [n_samples, n_features]
            Input data that will be transformed.
        """
        X = check_array(X, copy=self.copy)
        X -= self.min_
        X /= self.scale_
        return X