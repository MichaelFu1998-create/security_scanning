def get_batch(self, batch_size, next_states=False):
        """
        Samples a batch of the specified size according to priority.

        Args:
            batch_size: The batch size
            next_states: A boolean flag indicating whether 'next_states' values should be included

        Returns: A dict containing states, actions, rewards, terminals, internal states (and next states)

        """
        if batch_size > len(self.observations):
            raise TensorForceError(
                "Requested batch size is larger than observations in memory: increase config.first_update.")

        # Init empty states
        states = {name: np.zeros((batch_size,) + tuple(state['shape']), dtype=util.np_dtype(
            state['type'])) for name, state in self.states_spec.items()}
        internals = [np.zeros((batch_size,) + shape, dtype)
                     for shape, dtype in self.internals_spec]
        actions = {name: np.zeros((batch_size,) + tuple(action['shape']), dtype=util.np_dtype(action['type'])) for name, action in self.actions_spec.items()}
        terminal = np.zeros((batch_size,), dtype=util.np_dtype('bool'))
        reward = np.zeros((batch_size,), dtype=util.np_dtype('float'))
        if next_states:
            next_states = {name: np.zeros((batch_size,) + tuple(state['shape']), dtype=util.np_dtype(
                state['type'])) for name, state in self.states_spec.items()}
            next_internals = [np.zeros((batch_size,) + shape, dtype)
                              for shape, dtype in self.internals_spec]

        # Start with unseen observations
        unseen_indices = list(xrange(
            self.none_priority_index + self.observations._capacity - 1,
            len(self.observations) + self.observations._capacity - 1)
        )
        self.batch_indices = unseen_indices[:batch_size]

        # Get remaining observations using weighted sampling
        remaining = batch_size - len(self.batch_indices)
        if remaining:
            samples = self.observations.sample_minibatch(remaining)
            sample_indices = [i for i, o in samples]
            self.batch_indices += sample_indices

        # Shuffle
        np.random.shuffle(self.batch_indices)

        # Collect observations
        for n, index in enumerate(self.batch_indices):
            observation, _ = self.observations._memory[index]

            for name, state in states.items():
                state[n] = observation[0][name]
            for k, internal in enumerate(internals):
                internal[n] = observation[1][k]
            for name, action in actions.items():
                action[n] = observation[2][name]
            terminal[n] = observation[3]
            reward[n] = observation[4]
            if next_states:
                for name, next_state in next_states.items():
                    next_state[n] = observation[5][name]
                for k, next_internal in enumerate(next_internals):
                    next_internal[n] = observation[6][k]

        if next_states:
            return dict(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward,
                next_states=next_states,
                next_internals=next_internals
            )
        else:
            return dict(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward
            )