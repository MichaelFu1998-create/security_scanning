def load_value(self, key, binary=False):
        """
        Load an arbitrary value identified by `key`.

        :param str key: The key that identifies the value
        :return: The loaded value
        """
        with self.load_stream(key, binary=binary) as s:
            return s.read()