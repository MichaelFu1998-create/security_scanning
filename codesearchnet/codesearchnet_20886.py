def _step_to_marker_frame(self, frame_no, dt=None):
        '''Update the simulator to a specific frame of marker data.

        This method returns a generator of body states for the skeleton! This
        generator must be exhausted (e.g., by consuming this call in a for loop)
        for the simulator to work properly.

        This process involves the following steps:

        - Move the markers to their new location:
          - Detach from the skeleton
          - Update marker locations
          - Reattach to the skeleton
        - Detect ODE collisions
        - Yield the states of the bodies in the skeleton
        - Advance the ODE world one step

        Parameters
        ----------
        frame_no : int
            Step to this frame of marker data.
        dt : float, optional
            Step with this time duration. Defaults to ``self.dt``.

        Returns
        -------
        states : sequence of state tuples
            A generator of a sequence of one body state for the skeleton. This
            generator must be exhausted for the simulation to work properly.
        '''
        # update the positions and velocities of the markers.
        self.markers.detach()
        self.markers.reposition(frame_no)
        self.markers.attach(frame_no)

        # detect collisions.
        self.ode_space.collide(None, self.on_collision)

        # record the state of each skeleton body.
        states = self.skeleton.get_body_states()
        self.skeleton.set_body_states(states)

        # yield the current simulation state to our caller.
        yield states

        # update the ode world.
        self.ode_world.step(dt or self.dt)

        # clear out contact joints to prepare for the next frame.
        self.ode_contactgroup.empty()