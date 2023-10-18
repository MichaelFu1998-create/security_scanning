def step(self, substeps=2):
        '''Step the world forward by one frame.

        Parameters
        ----------
        substeps : int, optional
            Split the step into this many sub-steps. This helps to prevent the
            time delta for an update from being too large.
        '''
        self.frame_no += 1
        dt = self.dt / substeps
        for _ in range(substeps):
            self.ode_contactgroup.empty()
            self.ode_space.collide(None, self.on_collision)
            self.ode_world.step(dt)