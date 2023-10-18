def _wait_state(self, state, reward, terminal):
        """
        Wait until there is a state.
        """
        while state == [None] or not state:
             state, terminal, reward = self._execute(dict(key=0))

        return state, terminal, reward