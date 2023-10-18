def create_atomic_observe_operations(self, states, actions, internals, terminal, reward, index):
        """
        Returns the tf op to fetch when unbuffered observations are passed in.

        Args:
            states (any): One state (usually a value tuple) or dict of states if multiple states are expected.
            actions (any): One action (usually a value tuple) or dict of states if multiple actions are expected.
            internals (any): Internal list.
            terminal (bool): boolean indicating if the episode terminated after the observation.
            reward (float): scalar reward that resulted from executing the action.

        Returns: Tf op to fetch when `observe()` is called.
        """
        # Increment episode
        num_episodes = tf.count_nonzero(input_tensor=terminal, dtype=util.tf_dtype('int'))
        increment_episode = tf.assign_add(ref=self.episode, value=tf.to_int64(x=num_episodes))
        increment_global_episode = tf.assign_add(ref=self.global_episode, value=tf.to_int64(x=num_episodes))

        with tf.control_dependencies(control_inputs=(increment_episode, increment_global_episode)):
            # Stop gradients
            # Not using buffers here.
            states = util.map_tensors(fn=tf.stop_gradient, tensors=states)
            internals = util.map_tensors(fn=tf.stop_gradient, tensors=internals)
            actions = util.map_tensors(fn=tf.stop_gradient, tensors=actions)
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
            # Trivial operation to enforce control dependency.
            self.unbuffered_episode_output = self.global_episode + 0