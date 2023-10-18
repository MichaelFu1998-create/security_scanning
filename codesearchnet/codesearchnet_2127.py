def tf_observe_timestep(self, states, internals, actions, terminal, reward):
        """
        Creates and returns the op that - if frequency condition is hit - pulls a batch from the memory
        and does one optimization step.
        """
        # Store timestep in memory
        stored = self.memory.store(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward
        )

        # Periodic optimization
        with tf.control_dependencies(control_inputs=(stored,)):
            unit = self.update_mode['unit']
            batch_size = self.update_mode['batch_size']
            frequency = self.update_mode.get('frequency', batch_size)
            first_update = self.update_mode.get('first_update', 0)

            if unit == 'timesteps':
                # Timestep-based batch
                optimize = tf.logical_and(
                    x=tf.equal(x=(self.timestep % frequency), y=0),
                    y=tf.logical_and(
                        x=tf.greater_equal(x=self.timestep, y=batch_size),
                        y=tf.greater_equal(x=self.timestep, y=first_update)
                    )
                )

            elif unit == 'episodes':
                # Episode-based batch
                optimize = tf.logical_and(
                    x=tf.equal(x=(self.episode % frequency), y=0),
                    y=tf.logical_and(
                        # Only update once per episode increment.
                        x=tf.greater(x=tf.count_nonzero(input_tensor=terminal), y=0),
                        y=tf.logical_and(
                            x=tf.greater_equal(x=self.episode, y=batch_size),
                            y=tf.greater_equal(x=self.episode, y=first_update)
                        )
                    )
                )

            elif unit == 'sequences':
                # Timestep-sequence-based batch
                sequence_length = self.update_mode.get('length', 8)
                optimize = tf.logical_and(
                    x=tf.equal(x=(self.timestep % frequency), y=0),
                    y=tf.logical_and(
                        x=tf.greater_equal(x=self.timestep, y=(batch_size + sequence_length - 1)),
                        y=tf.greater_equal(x=self.timestep, y=first_update)
                    )
                )

            else:
                raise TensorForceError("Invalid update unit: {}.".format(unit))

            def true_fn():
                if unit == 'timesteps':
                    # Timestep-based batch
                    batch = self.memory.retrieve_timesteps(n=batch_size)
                elif unit == 'episodes':
                    # Episode-based batch
                    batch = self.memory.retrieve_episodes(n=batch_size)
                elif unit == 'sequences':
                    # Timestep-sequence-based batch
                    batch = self.memory.retrieve_sequences(n=batch_size, sequence_length=sequence_length)

                # Do not calculate gradients for memory-internal operations.
                batch = util.map_tensors(
                    fn=(lambda tensor: tf.stop_gradient(input=tensor)),
                    tensors=batch
                )

                optimize = self.fn_optimization(**batch)
                with tf.control_dependencies(control_inputs=(optimize,)):
                    return tf.logical_and(x=True, y=True)

            return tf.cond(pred=optimize, true_fn=true_fn, false_fn=tf.no_op)