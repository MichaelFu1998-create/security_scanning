def get_state_name(self):
        """
        Returns a textual representation of this Task's state.
        """
        state_name = []
        for state, name in list(self.state_names.items()):
            if self._has_state(state):
                state_name.append(name)
        return '|'.join(state_name)