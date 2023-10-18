def create_act_operations(self, states, internals, deterministic, independent, index):
        """
        Creates and stores tf operations that are fetched when calling act(): actions_output, internals_output and
        timestep_output.

        Args:
            states (dict): Dict of state tensors (each key represents one state space component).
            internals (dict): Dict of prior internal state tensors (each key represents one internal state component).
            deterministic: 0D (bool) tensor (whether to not use action exploration).
            independent (bool): 0D (bool) tensor (whether to store states/internals/action in local buffer).
        """

        # Optional variable noise
        operations = list()
        if self.variable_noise is not None and self.variable_noise > 0.0:
            # Initialize variables
            self.fn_actions_and_internals(
                states=states,
                internals=internals,
                deterministic=deterministic
            )

            noise_deltas = list()
            for variable in self.get_variables():
                noise_delta = tf.random_normal(shape=util.shape(variable), mean=0.0, stddev=self.variable_noise)
                noise_deltas.append(noise_delta)
                operations.append(variable.assign_add(delta=noise_delta))

        # Retrieve actions and internals
        with tf.control_dependencies(control_inputs=operations):
            self.actions_output, self.internals_output = self.fn_actions_and_internals(
                states=states,
                internals=internals,
                deterministic=deterministic
            )

        # Subtract variable noise
        # TODO this is an untested/incomplete feature and maybe should be removed for now.
        with tf.control_dependencies(control_inputs=[self.actions_output[name] for name in sorted(self.actions_output)]):
            operations = list()
            if self.variable_noise is not None and self.variable_noise > 0.0:
                for variable, noise_delta in zip(self.get_variables(), noise_deltas):
                    operations.append(variable.assign_sub(delta=noise_delta))

        # Actions exploration
        with tf.control_dependencies(control_inputs=operations):
            for name in sorted(self.actions_exploration):
                self.actions_output[name] = tf.cond(
                    pred=self.deterministic_input,
                    true_fn=(lambda: self.actions_output[name]),
                    false_fn=(lambda: self.fn_action_exploration(
                        action=self.actions_output[name],
                        exploration=self.actions_exploration[name],
                        action_spec=self.actions_spec[name]
                    ))
                )

        # Independent act not followed by observe.
        def independent_act():
            """
            Does not store state, action, internal in buffer. Hence, does not have any influence on learning.
            Does not increase timesteps.
            """
            return self.global_timestep

        # Normal act followed by observe, with additional operations.
        def normal_act():
            """
            Stores current states, internals and actions in buffer. Increases timesteps.
            """
            operations = list()

            batch_size = tf.shape(input=states[next(iter(sorted(states)))])[0]
            for name in sorted(states):
                operations.append(tf.assign(
                    ref=self.list_states_buffer[name][index, self.list_buffer_index[index]: self.list_buffer_index[index] + batch_size],
                    value=states[name]
                ))
            for name in sorted(internals):
                operations.append(tf.assign(
                    ref=self.list_internals_buffer[name][index, self.list_buffer_index[index]: self.list_buffer_index[index] + batch_size],
                    value=internals[name]
                ))
            for name in sorted(self.actions_output):
                operations.append(tf.assign(
                    ref=self.list_actions_buffer[name][index, self.list_buffer_index[index]: self.list_buffer_index[index] + batch_size],
                    value=self.actions_output[name]
                ))

            with tf.control_dependencies(control_inputs=operations):
                operations = list()

                operations.append(tf.assign(
                    ref=self.list_buffer_index[index: index+1],
                    value=tf.add(self.list_buffer_index[index: index+1], tf.constant([1]))
                ))

                    # Increment timestep
                operations.append(tf.assign_add(
                    ref=self.timestep,
                    value=tf.to_int64(x=batch_size)
                ))
                operations.append(tf.assign_add(
                    ref=self.global_timestep,
                    value=tf.to_int64(x=batch_size)
                ))

            with tf.control_dependencies(control_inputs=operations):
                # Trivial operation to enforce control dependency
                # TODO why not return no-op?
                return self.global_timestep + 0

        # Only increment timestep and update buffer if act not independent
        self.timestep_output = tf.cond(
            pred=independent,
            true_fn=independent_act,
            false_fn=normal_act
        )