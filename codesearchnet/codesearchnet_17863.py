def tk(self, k, x):
        """
        Evaluates an individual Chebyshev polynomial `k` in coordinate space
        with proper transformation given the window
        """
        weights = np.diag(np.ones(k+1))[k]
        return np.polynomial.chebyshev.chebval(self._x2c(x), weights)