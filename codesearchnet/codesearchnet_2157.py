def do_action(self, action):
        """Execute action, add a new tile, update the score & return the reward."""

        temp_state = np.rot90(self._state, action)
        reward = self._do_action_left(temp_state)
        self._state = np.rot90(temp_state, -action)
        self._score += reward

        self.add_random_tile()

        return reward