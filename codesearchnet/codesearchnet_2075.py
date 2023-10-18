def reset(self):
        """
        Resets the environment to its initialization state. This method needs to be called to start a
        new episode after the last episode ended.

        :return: initial state
        """
        self.level.reset()  # optional: episode=-1, seed=None
        return self.level.observations()[self.state_attribute]