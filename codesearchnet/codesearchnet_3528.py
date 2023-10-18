def load_stream(self, key, binary=False):
        """
        Return a managed file-like object from which the calling code can read
        previously-serialized data.

        :param key:
        :return: A managed stream-like object
        """
        value = self.load_value(key, binary=binary)
        yield io.BytesIO(value) if binary else io.StringIO(value)