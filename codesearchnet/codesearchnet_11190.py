def accuracy_gain(self):
        r"""Return gain in accuracy.

        The gain in accuracy is defined as:
        :math:`G(accuracy) = \frac{accuracy}{random~ accuracy}`

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        Returns
        -------
        float
            The gain in accuracy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.accuracy_gain()
        1.4325259515570934

        """
        if self.population() == 0:
            return float('NaN')
        random_accuracy = (self.cond_pos_pop() / self.population()) ** 2 + (
            self.cond_neg_pop() / self.population()
        ) ** 2
        return self.accuracy() / random_accuracy