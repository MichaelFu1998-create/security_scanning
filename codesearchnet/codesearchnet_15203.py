def _lml_optimal_scale(self):
        """
        Log of the marginal likelihood for optimal scale.

        Implementation for unrestricted LML::

        Returns
        -------
        lml : float
            Log of the marginal likelihood.
        """
        assert self._optimal["scale"]

        n = len(self._y)
        lml = -self._df * log2pi - self._df - n * log(self.scale)
        lml -= sum(npsum(log(D)) for D in self._D)
        return lml / 2