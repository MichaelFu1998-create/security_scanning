def atomic_observe(self, states, actions, internals, reward, terminal):
        """
        Utility method for unbuffered observing where each tuple is inserted into TensorFlow via
        a single session call, thus avoiding race conditions in multi-threaded mode.

        Observe full experience  tuplefrom the environment to learn from. Optionally pre-processes rewards
        Child classes should call super to get the processed reward
        EX: terminal, reward = super()...

        Args:
            states (any): One state (usually a value tuple) or dict of states if multiple states are expected.
            actions (any): One action (usually a value tuple) or dict of states if multiple actions are expected.
            internals (any): Internal list.
            terminal (bool): boolean indicating if the episode terminated after the observation.
            reward (float): scalar reward that resulted from executing the action.
        """
        # TODO probably unnecessary here.
        self.current_terminal = terminal
        self.current_reward = reward
        # print('action = {}'.format(actions))
        if self.unique_state:
            states = dict(state=states)
        if self.unique_action:
            actions = dict(action=actions)

        self.episode = self.model.atomic_observe(
            states=states,
            actions=actions,
            internals=internals,
            terminal=self.current_terminal,
            reward=self.current_reward
        )