def load_stream(self, key, binary=False):
        """
        :param str key: name of stream to load
        :param bool binary: Whether we should treat it as binary
        :return:
        """
        with open(os.path.join(self.uri, key), 'rb' if binary else 'r') as f:
            yield f