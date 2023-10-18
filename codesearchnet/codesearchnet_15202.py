def delta(self):
        """
        Variance ratio between ``K`` and ``I``.
        """

        v = float(self._logistic.value)

        if v > 0.0:
            v = 1 / (1 + exp(-v))
        else:
            v = exp(v)
            v = v / (v + 1.0)

        return min(max(v, epsilon.tiny), 1 - epsilon.tiny)