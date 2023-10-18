def execute(self, action):
        """
        Executes action, observes next state and reward.

        Args:
            actions: Action to execute.

        Returns:
            (Dict of) next state(s), boolean indicating terminal, and reward signal.
        """
        if self.env.game_over():
            return self.env.getScreenRGB(), True, 0

        action_space = self.env.getActionSet()
        reward = self.env.act(action_space[action])
        new_state = self.env.getScreenRGB()
        done = self.env.game_over()
        return new_state, done, reward