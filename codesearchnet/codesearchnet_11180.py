def to_dict(self):
        """Cast to dict.

        Returns
        -------
        dict
            The confusion table as a dict

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> import pprint
        >>> pprint.pprint(ct.to_dict())
        {'fn': 30, 'fp': 20, 'tn': 60, 'tp': 120}

        """
        return {'tp': self._tp, 'tn': self._tn, 'fp': self._fp, 'fn': self._fn}