def act(self, states, deterministic=False, independent=False, fetch_tensors=None, buffered=True, index=0):
        """
        Return action(s) for given state(s). States preprocessing and exploration are applied if
        configured accordingly.

        Args:
            states (any): One state (usually a value tuple) or dict of states if multiple states are expected.
            deterministic (bool): If true, no exploration and sampling is applied.
            independent (bool): If true, action is not followed by observe (and hence not included
                in updates).
            fetch_tensors (list): Optional String of named tensors to fetch
            buffered (bool): If true (default), states and internals are not returned but buffered
                with observes. Must be false for multi-threaded mode as we need atomic inserts.
        Returns:
            Scalar value of the action or dict of multiple actions the agent wants to execute.
            (fetched_tensors) Optional dict() with named tensors fetched
        """
        self.current_internals = self.next_internals

        if self.unique_state:
            self.current_states = dict(state=np.asarray(states))
        else:
            self.current_states = {name: np.asarray(states[name]) for name in sorted(states)}

        if fetch_tensors is not None:
            # Retrieve action
            self.current_actions, self.next_internals, self.timestep, self.fetched_tensors = self.model.act(
                states=self.current_states,
                internals=self.current_internals,
                deterministic=deterministic,
                independent=independent,
                fetch_tensors=fetch_tensors,
                index=index
            )

            if self.unique_action:
                return self.current_actions['action'], self.fetched_tensors
            else:
                return self.current_actions, self.fetched_tensors

        # Retrieve action.
        self.current_actions, self.next_internals, self.timestep = self.model.act(
            states=self.current_states,
            internals=self.current_internals,
            deterministic=deterministic,
            independent=independent,
            index=index
        )

        # Buffered mode only works single-threaded because buffer inserts
        # by multiple threads are non-atomic and can cause race conditions.
        if buffered:
            if self.unique_action:
                return self.current_actions['action']
            else:
                return self.current_actions
        else:
            if self.unique_action:
                return self.current_actions['action'], self.current_states, self.current_internals
            else:
                return self.current_actions, self.current_states, self.current_internals