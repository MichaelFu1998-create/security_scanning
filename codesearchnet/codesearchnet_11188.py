def fdr(self):
        r"""Return false discovery rate (FDR).

        False discovery rate is defined as :math:`\frac{fp}{fp + tp}`

        Cf. https://en.wikipedia.org/wiki/False_discovery_rate

        Returns
        -------
        float
            The false discovery rate of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fdr()
        0.14285714285714285

        """
        if self._fp + self._tp == 0:
            return float('NaN')
        return self._fp / (self._fp + self._tp)