def sample(self, random_state=None):
        r"""Sample from the specified distribution.

        Parameters
        ----------
        random_state : random_state
            Set the initial random state.

        Returns
        -------
        numpy.ndarray
            Sample.
        """
        from numpy_sugar import epsilon
        from numpy_sugar.linalg import sum2diag
        from numpy_sugar.random import multivariate_normal

        if random_state is None:
            random_state = RandomState()

        m = self._mean.value()
        K = self._cov.value().copy()

        sum2diag(K, +epsilon.small, out=K)

        return self._lik.sample(multivariate_normal(m, K, random_state), random_state)