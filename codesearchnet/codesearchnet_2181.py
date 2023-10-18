def act(self, states, internals, deterministic=False, independent=False, fetch_tensors=None, index=0):
        """
        Does a forward pass through the model to retrieve action (outputs) given inputs for state (and internal
        state, if applicable (e.g. RNNs))

        Args:
            states (dict): Dict of state values (each key represents one state space component).
            internals (dict): Dict of internal state values (each key represents one internal state component).
            deterministic (bool): If True, will not apply exploration after actions are calculated.
            independent (bool): If true, action is not followed by observe (and hence not included
                in updates).
            fetch_tensors (list): List of names of additional tensors (from the model's network) to fetch (and return).
            index: (int) index of the episode we want to produce the next action

        Returns:
            tuple:
                - Actual action-outputs (batched if state input is a batch).
                - Actual values of internal states (if applicable) (batched if state input is a batch).
                - The timestep (int) after calculating the (batch of) action(s).
        """
        name = next(iter(states))
        state = np.asarray(states[name])
        batched = (state.ndim != len(self.states_spec[name]['unprocessed_shape']))
        if batched:
            assert state.shape[0] <= self.batching_capacity

        fetches = [self.actions_output, self.internals_output, self.timestep_output]
        if self.network is not None and fetch_tensors is not None:
            for name in fetch_tensors:
                valid, tensor = self.network.get_named_tensor(name)
                if valid:
                    fetches.append(tensor)
                else:
                    keys = self.network.get_list_of_named_tensor()
                    raise TensorForceError('Cannot fetch named tensor "{}", Available {}.'.format(name, keys))

        # feed_dict[self.deterministic_input] = deterministic
        feed_dict = self.get_feed_dict(
            states=states,
            internals=internals,
            deterministic=deterministic,
            independent=independent,
            index=index
        )

        fetch_list = self.monitored_session.run(fetches=fetches, feed_dict=feed_dict)
        actions, internals, timestep = fetch_list[0:3]

        # Extract the first (and only) action/internal from the batch to make return values non-batched
        if not batched:
            actions = {name: actions[name][0] for name in sorted(actions)}
            internals = {name: internals[name][0] for name in sorted(internals)}

        if self.network is not None and fetch_tensors is not None:
            fetch_dict = dict()
            for index_, tensor in enumerate(fetch_list[3:]):
                name = fetch_tensors[index_]
                fetch_dict[name] = tensor
            return actions, internals, timestep, fetch_dict
        else:
            return actions, internals, timestep