def save_stream(self, key, binary=False):
        """
        Yield a file object representing `key`

        :param str key: The file to save to
        :param bool binary: Whether we should treat it as binary
        :return:
        """
        mode = 'wb' if binary else 'w'
        with open(os.path.join(self.uri, key), mode) as f:
            yield f