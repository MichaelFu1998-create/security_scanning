def _updateType(self):
        """Make sure that the class behaves like the data structure that it
        is, so that we don't get a ListFile trying to represent a dict."""
        data = self._data()
        # Change type if needed
        if isinstance(data, dict) and isinstance(self, ListFile):
            self.__class__ = DictFile
        elif isinstance(data, list) and isinstance(self, DictFile):
            self.__class__ = ListFile