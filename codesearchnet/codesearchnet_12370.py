def predict(self, X):
        """Predict class labels for samples in X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Samples.
        """
        if isinstance(X[0], list):
            return [self.estimator.tag(x) for x in X]
        return self.estimator.tag(X)