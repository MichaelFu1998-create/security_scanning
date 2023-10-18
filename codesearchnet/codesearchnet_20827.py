def set_body_states(self, states):
        '''Set the states of some bodies in the world.

        Parameters
        ----------
        states : sequence of states
            A complete state tuple for one or more bodies in the world. See
            :func:`get_body_states`.
        '''
        for state in states:
            self.get_body(state.name).state = state