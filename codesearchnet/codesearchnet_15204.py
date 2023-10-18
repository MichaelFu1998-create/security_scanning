def _lml_arbitrary_scale(self):
        """
        Log of the marginal likelihood for arbitrary scale.

        Returns
        -------
        lml : float
            Log of the marginal likelihood.
        """
        s = self.scale
        D = self._D
        n = len(self._y)
        lml = -self._df * log2pi - n * log(s)
        lml -= sum(npsum(log(d)) for d in D)
        d = (mTQ - yTQ for (mTQ, yTQ) in zip(self._mTQ, self._yTQ))
        lml -= sum((i / j) @ i for (i, j) in zip(d, D)) / s

        return lml / 2