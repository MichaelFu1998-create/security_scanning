def state(self, state):
        '''Set the state of this body.

        Parameters
        ----------
        state : BodyState tuple
            The desired state of the body.
        '''
        assert self.name == state.name, \
            'state name "{}" != body name "{}"'.format(state.name, self.name)
        self.position = state.position
        self.quaternion = state.quaternion
        self.linear_velocity = state.linear_velocity
        self.angular_velocity = state.angular_velocity