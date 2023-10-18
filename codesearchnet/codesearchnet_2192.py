def states(self):
        """
        Return the state space. Might include subdicts if multiple states are
        available simultaneously.

        Returns: dict of state properties (shape and type).

        """
        screen = self.env.getScreenRGB()
        return dict(shape=screen.shape, type='int')