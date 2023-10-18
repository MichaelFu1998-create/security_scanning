def transform(self, X):
        '''
        Transforms X according to the linear transformation corresponding to
        shifting the input eigenvalues to all be at least ``self.min_eig``.

        Parameters
        ----------
        X : array, shape [n_test, n]
            The test similarities to training points.

        Returns
        -------
        Xt : array, shape [n_test, n]
            The transformed test similarites to training points. Only different
            from X if X is the training data.
        '''
        n = self.train_.shape[0]
        if X.ndim != 2 or X.shape[1] != n:
            msg = "X should have {} columns, the number of samples at fit time"
            raise TypeError(msg.format(n))

        if self.copy:
            X = X.copy()

        if self.shift_ != 0 and X is self.train_ or (
                X.shape == self.train_.shape and np.allclose(X, self.train_)):
            X[xrange(n), xrange(n)] += self.shift_
        return X