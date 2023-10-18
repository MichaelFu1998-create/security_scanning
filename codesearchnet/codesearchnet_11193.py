def mcc(self):
        r"""Return Matthews correlation coefficient (MCC).

        The Matthews correlation coefficient is defined in
        :cite:`Matthews:1975` as:
        :math:`\frac{(tp \cdot tn) - (fp \cdot fn)}
        {\sqrt{(tp + fp)(tp + fn)(tn + fp)(tn + fn)}}`

        This is equivalent to the geometric mean of informedness and
        markedness, defined above.

        Cf. https://en.wikipedia.org/wiki/Matthews_correlation_coefficient

        Returns
        -------
        float
            The Matthews correlation coefficient of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.mcc()
        0.5367450401216932

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
        return ((self._tp * self._tn) - (self._fp * self._fn)) / math.sqrt(
            (self._tp + self._fp)
            * (self._tp + self._fn)
            * (self._tn + self._fp)
            * (self._tn + self._fn)
        )