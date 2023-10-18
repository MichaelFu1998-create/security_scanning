def fit_transform(self, X, y=None):
        '''
        Flips the negative eigenvalues of X.

        Parameters
        ----------
        X : array, shape [n, n]
            The *symmetric* input similarities. If X is asymmetric, it will be
            treated as if it were symmetric based on its lower-triangular part.

        Returns
        -------
        Xt : array, shape [n, n]
            The transformed training similarities.
        '''
        n = X.shape[0]
        if X.shape != (n, n):
            raise TypeError("Input must be a square matrix.")

        memory = get_memory(self.memory)
        discard_X = not self.copy and self.negatives_likely
        vals, vecs = memory.cache(scipy.linalg.eigh, ignore=['overwrite_a'])(
            X, overwrite_a=discard_X)
        vals = vals[:, None]

        self.clip_ = np.dot(vecs, np.sign(vals) * vecs.T)

        if discard_X or vals[0, 0] < 0:
            del X
            np.abs(vals, out=vals)
            X = np.dot(vecs, vals * vecs.T)
            del vals, vecs

            # should be symmetric, but make sure because floats
            X = Symmetrize(copy=False).fit_transform(X)
        return X