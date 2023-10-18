def transform(self, X):
        '''
        Turns distances into RBF values.

        Parameters
        ----------
        X : array
            The raw pairwise distances.

        Returns
        -------
        X_rbf : array of same shape as X
            The distances in X passed through the RBF kernel.
        '''
        X = check_array(X)
        X_rbf = np.empty_like(X) if self.copy else X

        X_in = X
        if not self.squared:
            np.power(X_in, 2, out=X_rbf)
            X_in = X_rbf

        if self.scale_by_median:
            scale = self.median_ if self.squared else self.median_ ** 2
            gamma = self.gamma * scale
        else:
            gamma = self.gamma
        np.multiply(X_in, -gamma, out=X_rbf)

        np.exp(X_rbf, out=X_rbf)
        return X_rbf