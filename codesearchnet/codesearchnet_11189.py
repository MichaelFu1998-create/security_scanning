def accuracy(self):
        r"""Return accuracy.

        Accuracy is defined as :math:`\frac{tp + tn}{population}`

        Cf. https://en.wikipedia.org/wiki/Accuracy

        Returns
        -------
        float
            The accuracy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.accuracy()
        0.782608695652174

        """
        if self.population() == 0:
            return float('NaN')
        return (self._tp + self._tn) / self.population()