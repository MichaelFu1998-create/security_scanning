def npv(self):
        r"""Return negative predictive value (NPV).

        NPV is defined as :math:`\frac{tn}{tn + fn}`

        Cf. https://en.wikipedia.org/wiki/Negative_predictive_value

        Returns
        -------
        float
            The negative predictive value of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.npv()
        0.6666666666666666

        """
        if self._tn + self._fn == 0:
            return float('NaN')
        return self._tn / (self._tn + self._fn)