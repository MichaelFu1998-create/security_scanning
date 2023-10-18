def recall(self):
        r"""Return recall.

        Recall is defined as :math:`\frac{tp}{tp + fn}`

        AKA sensitivity

        AKA true positive rate (TPR)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall

        Cf. https://en.wikipedia.org/wiki/Sensitivity_(test)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Recall

        Returns
        -------
        float
            The recall of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.recall()
        0.8

        """
        if self._tp + self._fn == 0:
            return float('NaN')
        return self._tp / (self._tp + self._fn)