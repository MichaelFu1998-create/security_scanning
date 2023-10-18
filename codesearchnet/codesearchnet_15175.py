def eigh(self):
        """
        Eigen decomposition of K.

        Returns
        -------
        S : ndarray
            The eigenvalues in ascending order, each repeated according to its
            multiplicity.
        U : ndarray
            Normalized eigenvectors.
        """
        from numpy.linalg import svd

        if self._cache["eig"] is not None:
            return self._cache["eig"]

        U, S = svd(self.L)[:2]
        S *= S
        S += self._epsilon
        self._cache["eig"] = S, U

        return self._cache["eig"]