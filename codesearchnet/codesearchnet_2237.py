def tf_step(self, time, variables, source_variables, **kwargs):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            source_variables: List of source variables to synchronize with.
            **kwargs: Additional arguments, not used.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """
        assert all(util.shape(source) == util.shape(target) for source, target in zip(source_variables, variables))

        last_sync = tf.get_variable(
            name='last-sync',
            shape=(),
            dtype=tf.int64,
            initializer=tf.constant_initializer(value=(-self.sync_frequency), dtype=tf.int64),
            trainable=False
        )

        def sync():
            deltas = list()
            for source_variable, target_variable in zip(source_variables, variables):
                delta = self.update_weight * (source_variable - target_variable)
                deltas.append(delta)

            applied = self.apply_step(variables=variables, deltas=deltas)
            last_sync_updated = last_sync.assign(value=time)

            with tf.control_dependencies(control_inputs=(applied, last_sync_updated)):
                # Trivial operation to enforce control dependency
                return [delta + 0.0 for delta in deltas]

        def no_sync():
            deltas = list()
            for variable in variables:
                delta = tf.zeros(shape=util.shape(variable))
                deltas.append(delta)
            return deltas

        do_sync = (time - last_sync >= self.sync_frequency)
        return tf.cond(pred=do_sync, true_fn=sync, false_fn=no_sync)