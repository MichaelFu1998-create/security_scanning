def transform(self, X):
        '''
        Transforms X according to the linear transformation corresponding to
        flipping the input eigenvalues.

        Parameters
        ----------
        X : array, shape [n_test, n]
            The test similarities to training points.

        Returns
        -------
        Xt : array, shape [n_test, n]
            The transformed test similarites to training points.
        '''
        n = self.flip_.shape[0]
        if X.ndim != 2 or X.shape[1] != n:
            msg = "X should have {} columns, the number of samples at fit time"
            raise TypeError(msg.format(self.flip_.shape[0]))
        return np.dot(X, self.flip_)