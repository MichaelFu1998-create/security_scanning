def to_tuple(self):
        """Cast to tuple.

        Returns
        -------
        tuple
            The confusion table as a 4-tuple (tp, tn, fp, fn)

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.to_tuple()
        (120, 60, 20, 30)

        """
        return self._tp, self._tn, self._fp, self._fn