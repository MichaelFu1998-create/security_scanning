def insert(self, index, value):
        """
        Insert object before index.

        :param int index: index to insert in
        :param string value: path to insert
        """
        self._list.insert(index, value)
        self._sync()