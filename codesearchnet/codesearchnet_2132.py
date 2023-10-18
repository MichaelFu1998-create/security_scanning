def reset(self):
        """
        Resets the agent to its initial state (e.g. on experiment start). Updates the Model's internal episode and
        time step counter, internal states, and resets preprocessors.
        """
        self.episode, self.timestep, self.next_internals = self.model.reset()
        self.current_internals = self.next_internals