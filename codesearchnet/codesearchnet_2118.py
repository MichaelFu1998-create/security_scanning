def execute(self, action):
        """
        Executes action, observes next state and reward.

        Args:
            actions: Actions to execute.

        Returns:
            Tuple of (next state, bool indicating terminal, reward)
        """
        next_state, rew, done, _ = self.env.step(action)
        return next_state, rew, done