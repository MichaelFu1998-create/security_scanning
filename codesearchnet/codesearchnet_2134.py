def observe(self, terminal, reward, index=0):
        """
        Observe experience from the environment to learn from. Optionally pre-processes rewards
        Child classes should call super to get the processed reward
        EX: terminal, reward = super()...

        Args:
            terminal (bool): boolean indicating if the episode terminated after the observation.
            reward (float): scalar reward that resulted from executing the action.
        """
        self.current_terminal = terminal
        self.current_reward = reward

        if self.batched_observe:
            # Batched observe for better performance with Python.
            self.observe_terminal[index].append(self.current_terminal)
            self.observe_reward[index].append(self.current_reward)

            if self.current_terminal or len(self.observe_terminal[index]) >= self.batching_capacity:
                self.episode = self.model.observe(
                    terminal=self.observe_terminal[index],
                    reward=self.observe_reward[index],
                    index=index
                )
                self.observe_terminal[index] = list()
                self.observe_reward[index] = list()

        else:
            self.episode = self.model.observe(
                terminal=self.current_terminal,
                reward=self.current_reward
            )