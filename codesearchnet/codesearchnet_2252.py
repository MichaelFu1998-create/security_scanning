def tf_step(self, time, variables, **kwargs):
        """
        Keyword Args:
            arguments: Dict of arguments for passing to fn_loss as **kwargs.
            fn_loss: A callable taking arguments as kwargs and returning the loss op of the current model.
        """
        arguments = kwargs["arguments"]
        fn_loss = kwargs["fn_loss"]
        loss = fn_loss(**arguments)

        # Force loss value to be calculated.
        with tf.control_dependencies(control_inputs=(loss,)):
            # Trivial operation to enforce control dependency
            previous_variables = [variable + 0.0 for variable in variables]

        # The actual tensorflow minimize op.
        with tf.control_dependencies(control_inputs=previous_variables):
            applied = self.tf_optimizer.minimize(loss=loss, var_list=variables)  # colocate_gradients_with_ops=True

        # Return deltas after actually having change the variables.
        with tf.control_dependencies(control_inputs=(applied,)):
            return [
                variable - previous_variable
                for variable, previous_variable in zip(variables, previous_variables)
            ]