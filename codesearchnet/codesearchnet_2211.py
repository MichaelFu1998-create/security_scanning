def tf_retrieve_indices(self, indices):
        """
        Fetches experiences for given indices.

        Args:
            indices: Index tensor

        Returns: Batch of experiences
        """
        states = dict()
        for name in sorted(self.states_memory):
            states[name] = tf.gather(params=self.states_memory[name], indices=indices)

        internals = dict()
        for name in sorted(self.internals_memory):
            internals[name] = tf.gather(params=self.internals_memory[name], indices=indices)

        actions = dict()
        for name in sorted(self.actions_memory):
            actions[name] = tf.gather(params=self.actions_memory[name], indices=indices)

        terminal = tf.gather(params=self.terminal_memory, indices=indices)
        reward = tf.gather(params=self.reward_memory, indices=indices)

        if self.include_next_states:
            assert util.rank(indices) == 1
            next_indices = (indices + 1) % self.capacity

            next_states = dict()
            for name in sorted(self.states_memory):
                next_states[name] = tf.gather(params=self.states_memory[name], indices=next_indices)

            next_internals = dict()
            for name in sorted(self.internals_memory):
                next_internals[name] = tf.gather(params=self.internals_memory[name], indices=next_indices)

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