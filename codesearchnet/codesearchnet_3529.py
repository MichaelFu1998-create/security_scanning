def save_state(self, state, key):
        """
        Save a state to storage.

        :param manticore.core.StateBase state:
        :param str key:
        :return:
        """
        with self.save_stream(key, binary=True) as f:
            self._serializer.serialize(state, f)