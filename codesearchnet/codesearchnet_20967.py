def add_data(self, data):
        """ Add POST data.

        Args:
            data (dict): key => value dictionary
        """
        if not self._data:
            self._data = {}
        self._data.update(data)