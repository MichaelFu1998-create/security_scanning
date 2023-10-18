def population(self):
        """Return population, N.

        Returns
        -------
        int
            The population (N) of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.population()
        230

        """
        return self._tp + self._tn + self._fp + self._fn