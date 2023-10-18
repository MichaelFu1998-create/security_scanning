def get(self, item, alt=None):
        """
        Standard dict-like .get() method.

        Args:
            item (str): See :meth:`.__getitem__` for details.
            alt (default None): Alternative value, if item is not found.

        Returns:
            obj: `item` or `alt`, if item is not found.
        """
        try:
            val = self[item]
        except ValueError:
            return alt

        return val if val is not None else alt