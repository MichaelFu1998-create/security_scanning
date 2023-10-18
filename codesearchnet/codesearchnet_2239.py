def tf_step(self, time, variables, **kwargs):
        """
        Keyword Args:
            global_variables: List of global variables to apply the proposed optimization step to.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """

        global_variables = kwargs["global_variables"]

        assert all(
            util.shape(global_variable) == util.shape(local_variable)
            for global_variable, local_variable in zip(global_variables, variables)
        )

        local_deltas = self.optimizer.step(time=time, variables=variables, **kwargs)

        with tf.control_dependencies(control_inputs=local_deltas):
            applied = self.optimizer.apply_step(variables=global_variables, deltas=local_deltas)

        with tf.control_dependencies(control_inputs=(applied,)):
            update_deltas = list()
            for global_variable, local_variable in zip(global_variables, variables):
                delta = global_variable - local_variable
                update_deltas.append(delta)

            applied = self.apply_step(variables=variables, deltas=update_deltas)

            # TODO: Update time, episode, etc (like in Synchronization)?

        with tf.control_dependencies(control_inputs=(applied,)):
            return [local_delta + update_delta for local_delta, update_delta in zip(local_deltas, update_deltas)]