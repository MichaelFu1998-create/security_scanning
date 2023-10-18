def _named_stream(self, name, binary=False):
        """
        Create an indexed output stream i.e. 'test_00000001.name'

        :param name: Identifier for the stream
        :return: A context-managed stream-like object
        """
        with self._store.save_stream(self._named_key(name), binary=binary) as s:
            yield s