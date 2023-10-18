def tf_retrieve_indices(self, buffer_elements, priority_indices):
        """
        Fetches experiences for given indices by combining entries from buffer
        which have no priorities, and entries from priority memory.

        Args:
            buffer_elements: Number of buffer elements to retrieve
            priority_indices: Index tensor for priority memory

        Returns: Batch of experiences
        """
        states = dict()
        buffer_start = self.buffer_index - buffer_elements
        buffer_end = self.buffer_index

        # Fetch entries from respective memories, concat.
        for name in sorted(self.states_memory):
            buffer_state_memory = self.states_buffer[name]
            # Slicing is more efficient than gathering, and buffer elements are always
            # fetched using contiguous indices.
            buffer_states = buffer_state_memory[buffer_start:buffer_end]
            # Memory indices are obtained via priority sampling, hence require gather.
            memory_states = tf.gather(params=self.states_memory[name], indices=priority_indices)
            states[name] = tf.concat(values=(buffer_states, memory_states), axis=0)

        internals = dict()
        for name in sorted(self.internals_memory):
            internal_buffer_memory = self.internals_buffer[name]
            buffer_internals = internal_buffer_memory[buffer_start:buffer_end]
            memory_internals = tf.gather(params=self.internals_memory[name], indices=priority_indices)
            internals[name] = tf.concat(values=(buffer_internals, memory_internals), axis=0)

        actions = dict()
        for name in sorted(self.actions_memory):
            action_buffer_memory = self.actions_buffer[name]
            buffer_action = action_buffer_memory[buffer_start:buffer_end]
            memory_action = tf.gather(params=self.actions_memory[name], indices=priority_indices)
            actions[name] = tf.concat(values=(buffer_action, memory_action), axis=0)

        buffer_terminal = self.terminal_buffer[buffer_start:buffer_end]
        priority_terminal = tf.gather(params=self.terminal_memory, indices=priority_indices)
        terminal = tf.concat(values=(buffer_terminal, priority_terminal), axis=0)

        buffer_reward = self.reward_buffer[buffer_start:buffer_end]
        priority_reward = tf.gather(params=self.reward_memory, indices=priority_indices)
        reward = tf.concat(values=(buffer_reward, priority_reward), axis=0)

        if self.include_next_states:
            assert util.rank(priority_indices) == 1
            next_priority_indices = (priority_indices + 1) % self.capacity
            next_buffer_start = (buffer_start + 1) % self.buffer_size
            next_buffer_end = (buffer_end + 1) % self.buffer_size

            next_states = dict()
            for name in sorted(self.states_memory):
                buffer_state_memory = self.states_buffer[name]
                buffer_next_states = buffer_state_memory[next_buffer_start:next_buffer_end]
                memory_next_states = tf.gather(params=self.states_memory[name], indices=next_priority_indices)
                next_states[name] = tf.concat(values=(buffer_next_states, memory_next_states), axis=0)

            next_internals = dict()
            for name in sorted(self.internals_memory):
                buffer_internal_memory = self.internals_buffer[name]
                buffer_next_internals = buffer_internal_memory[next_buffer_start:next_buffer_end]
                memory_next_internals = tf.gather(params=self.internals_memory[name], indices=next_priority_indices)
                next_internals[name] = tf.concat(values=(buffer_next_internals, memory_next_internals), axis=0)

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