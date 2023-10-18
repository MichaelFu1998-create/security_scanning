def load_state(self, key, delete=True):
        """
        Load a state from storage.

        :param key: key that identifies state
        :rtype: manticore.core.StateBase
        """
        with self.load_stream(key, binary=True) as f:
            state = self._serializer.deserialize(f)
            if delete:
                self.rm(key)
            return state