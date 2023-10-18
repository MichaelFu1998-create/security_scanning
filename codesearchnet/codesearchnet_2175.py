def create_observe_operations(self, terminal, reward, index):
        """
        Returns the tf op to fetch when an observation batch is passed in (e.g. an episode's rewards and
        terminals). Uses the filled tf buffers for states, actions and internals to run
        the tf_observe_timestep (model-dependent), resets buffer index and increases counters (episodes,
        timesteps).

        Args:
            terminal: The 1D tensor (bool) of terminal signals to process (more than one True within that list is ok).
            reward: The 1D tensor (float) of rewards to process.

        Returns: Tf op to fetch when `observe()` is called.
        """
        # Increment episode
        num_episodes = tf.count_nonzero(input_tensor=terminal, dtype=util.tf_dtype('int'))
        increment_episode = tf.assign_add(ref=self.episode, value=tf.to_int64(x=num_episodes))
        increment_global_episode = tf.assign_add(ref=self.global_episode, value=tf.to_int64(x=num_episodes))

        with tf.control_dependencies(control_inputs=(increment_episode, increment_global_episode)):
            # Stop gradients
            fn = (lambda x: tf.stop_gradient(input=x[:self.list_buffer_index[index]]))
            states = util.map_tensors(fn=fn, tensors=self.list_states_buffer, index=index)
            internals = util.map_tensors(fn=fn, tensors=self.list_internals_buffer, index=index)
            actions = util.map_tensors(fn=fn, tensors=self.list_actions_buffer, index=index)
            terminal = tf.stop_gradient(input=terminal)
            reward = tf.stop_gradient(input=reward)

            # Observation
            observation = self.fn_observe_timestep(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward
            )

        with tf.control_dependencies(control_inputs=(observation,)):
            # Reset buffer index.
            reset_index = tf.assign(ref=self.list_buffer_index[index], value=0)

        with tf.control_dependencies(control_inputs=(reset_index,)):
            # Trivial operation to enforce control dependency.
            self.episode_output = self.global_episode + 0

        self.list_buffer_index_reset_op = tf.group(
            *(tf.assign(ref=self.list_buffer_index[n], value=0) for n in range(self.num_parallel))
        )