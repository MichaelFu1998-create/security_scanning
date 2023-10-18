def fit(self, X, y=None):
        '''
        Learn the transformation to shifted eigenvalues. Only depends
        on the input dimension.

        Parameters
        ----------
        X : array, shape [n, n]
            The *symmetric* input similarities.
        '''
        n = X.shape[0]
        if X.shape != (n, n):
            raise TypeError("Input must be a square matrix.")

        self.train_ = X

        memory = get_memory(self.memory)
        lo, = memory.cache(scipy.linalg.eigvalsh)(X, eigvals=(0, 0))
        self.shift_ = max(self.min_eig - lo, 0)

        return self