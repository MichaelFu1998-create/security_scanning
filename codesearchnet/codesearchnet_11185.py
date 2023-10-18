def specificity(self):
        r"""Return specificity.

        Specificity is defined as :math:`\frac{tn}{tn + fp}`

        AKA true negative rate (TNR)

        Cf. https://en.wikipedia.org/wiki/Specificity_(tests)

        Returns
        -------
        float
            The specificity of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.specificity()
        0.75

        """
        if self._tn + self._fp == 0:
            return float('NaN')
        return self._tn / (self._tn + self._fp)