def json(self):
        """
        Return JSON representation of object.
        """
        data = {}
        for item in self._data:
            if isinstance(self._data[item], filetree):
                data[item] = self._data[item].json()
            else:
                data[item] = self._data[item]
        return data