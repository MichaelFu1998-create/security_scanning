def save_state(self, state, state_id=None):
        """
        Save a state to storage, return identifier.

        :param state: The state to save
        :param int state_id: If not None force the state id potentially overwriting old states
        :return: New state id
        :rtype: int
        """
        assert isinstance(state, StateBase)
        if state_id is None:
            state_id = self._get_id()
        else:
            self.rm_state(state_id)

        self._store.save_state(state, f'{self._prefix}{state_id:08x}{self._suffix}')
        return state_id