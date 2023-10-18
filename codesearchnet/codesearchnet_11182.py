def precision(self):
        r"""Return precision.

        Precision is defined as :math:`\frac{tp}{tp + fp}`

        AKA positive predictive value (PPV)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Precision

        Returns
        -------
        float
            The precision of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.precision()
        0.8571428571428571

        """
        if self._tp + self._fp == 0:
            return float('NaN')
        return self._tp / (self._tp + self._fp)