def precision_gain(self):
        r"""Return gain in precision.

        The gain in precision is defined as:
        :math:`G(precision) = \frac{precision}{random~ precision}`

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        Returns
        -------
        float
            The gain in precision of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.precision_gain()
        1.3142857142857143

        """
        if self.population() == 0:
            return float('NaN')
        random_precision = self.cond_pos_pop() / self.population()
        return self.precision() / random_precision