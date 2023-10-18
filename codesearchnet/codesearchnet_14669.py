def _construct_key(self, values):
        """Return a dictionary representing a key from a list of columns
        and a tuple of values
        """
        key = {}
        for column, value in zip(self.keys.columns, values):
            key.update({column.name: value})
        return key