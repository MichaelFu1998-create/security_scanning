def save_stream(self, key, binary=False):
        """
        Return a managed file-like object into which the calling code can write
        arbitrary data.

        :param key:
        :return: A managed stream-like object
        """
        s = io.BytesIO() if binary else io.StringIO()
        yield s
        self.save_value(key, s.getvalue())