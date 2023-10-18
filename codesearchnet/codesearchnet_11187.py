def fallout(self):
        r"""Return fall-out.

        Fall-out is defined as :math:`\frac{fp}{fp + tn}`

        AKA false positive rate (FPR)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Fall-out

        Returns
        -------
        float
            The fall-out of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fallout()
        0.25

        """
        if self._fp + self._tn == 0:
            return float('NaN')
        return self._fp / (self._fp + self._tn)