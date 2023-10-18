def significance(self):
        r"""Return the significance, :math:`\chi^{2}`.

        Significance is defined as:
        :math:`\chi^{2} =
        \frac{(tp \cdot tn - fp \cdot fn)^{2} (tp + tn + fp + fn)}
        {((tp + fp)(tp + fn)(tn + fp)(tn + fn)}`

        Also: :math:`\chi^{2} = MCC^{2} \cdot n`

        Cf. https://en.wikipedia.org/wiki/Pearson%27s_chi-square_test

        Returns
        -------
        float
            The significance of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.significance()
        66.26190476190476

        """
        if (
            (
                (self._tp + self._fp)
                * (self._tp + self._fn)
                * (self._tn + self._fp)
                * (self._tn + self._fn)
            )
        ) == 0:
            return float('NaN')
        return (
            (self._tp * self._tn - self._fp * self._fn) ** 2
            * (self._tp + self._tn + self._fp + self._fn)
        ) / (
            (self._tp + self._fp)
            * (self._tp + self._fn)
            * (self._tn + self._fp)
            * (self._tn + self._fn)
        )