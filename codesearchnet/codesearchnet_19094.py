def fit(self, X, y=None):
        '''
        Learn the linear transformation to flipped eigenvalues.

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
        vals = vals[:, None]

        self.flip_ = np.dot(vecs, np.sign(vals) * vecs.T)
        return self