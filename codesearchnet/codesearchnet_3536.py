def load_state(self, state_id, delete=True):
        """
        Load a state from storage identified by `state_id`.

        :param state_id: The state reference of what to load
        :return: The deserialized state
        :rtype: State
        """
        return self._store.load_state(f'{self._prefix}{state_id:08x}{self._suffix}', delete=delete)