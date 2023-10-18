def tf_step(self, time, variables, arguments, fn_reference=None, **kwargs):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            arguments: Dict of arguments for callables, like fn_loss.
            fn_reference: A callable returning the reference values, in case of a comparative loss.
            **kwargs: Additional arguments passed on to the internal optimizer.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """

        # Set reference to compare with at each optimization step, in case of a comparative loss.
        arguments['reference'] = fn_reference(**arguments)

        # First step
        deltas = self.optimizer.step(time=time, variables=variables, arguments=arguments, **kwargs)

        if self.unroll_loop:
            # Unrolled for loop
            for _ in xrange(self.num_steps - 1):
                with tf.control_dependencies(control_inputs=deltas):
                    step_deltas = self.optimizer.step(time=time, variables=variables, arguments=arguments, **kwargs)
                    deltas = [delta1 + delta2 for delta1, delta2 in zip(deltas, step_deltas)]

            return deltas

        else:
            # TensorFlow while loop
            def body(iteration, deltas):
                with tf.control_dependencies(control_inputs=deltas):
                    step_deltas = self.optimizer.step(time=time, variables=variables, arguments=arguments, **kwargs)
                    deltas = [delta1 + delta2 for delta1, delta2 in zip(deltas, step_deltas)]
                    return iteration + 1, deltas

            def cond(iteration, deltas):
                return iteration < self.num_steps - 1

            _, deltas = tf.while_loop(cond=cond, body=body, loop_vars=(0, deltas))

            return deltas