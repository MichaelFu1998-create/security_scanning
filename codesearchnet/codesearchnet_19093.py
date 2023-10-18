def fit(self, X, y=None):
        '''
        Learn the linear transformation to clipped eigenvalues.

        Note that if min_eig isn't zero and any of the original eigenvalues
        were exactly zero, this will leave those eigenvalues as zero.

        Parameters
        ----------
        X : array, shape [n, n]
            The *symmetric* input similarities. If X is asymmetric, it will be
            treated as if it were symmetric based on its lower-triangular part.
        '''
        n = X.shape[0]
        if X.shape != (n, n):
            raise TypeError("Input must be a square matrix.")

        # TODO: only get negative eigs somehow?
        memory = get_memory(self.memory)
        vals, vecs = memory.cache(scipy.linalg.eigh, ignore=['overwrite_a'])(
            X, overwrite_a=not self.copy)
        vals = vals.reshape(-1, 1)

        if self.min_eig == 0:
            inner = vals > self.min_eig
        else:
            with np.errstate(divide='ignore'):
                inner = np.where(vals >= self.min_eig, 1,
                                 np.where(vals == 0, 0, self.min_eig / vals))

        self.clip_ = np.dot(vecs, inner * vecs.T)
        return self