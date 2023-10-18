def at(self, index):
        """Get the object at an :paramref:`index`.

        :param int index: the index of the object
        :return: the object at :paramref:`index`
        """
        keys = list(self._items.keys())
        key = keys[index]
        return self[key]