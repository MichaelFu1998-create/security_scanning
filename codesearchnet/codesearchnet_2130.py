def tf_step(
        self,
        time,
        variables,
        arguments,
        fn_loss,
        fn_reference,
        **kwargs
    ):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            arguments: Dict of arguments for callables, like fn_loss.
            fn_loss: A callable returning the loss of the current model.
            fn_reference: A callable returning the reference values, in case of a comparative loss.
            **kwargs: Additional arguments passed on to the internal optimizer.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """

        # Set reference to compare with at each optimization step, in case of a comparative loss.
        arguments['reference'] = fn_reference(**arguments)

        # Negative value since line search maximizes.
        loss_before = -fn_loss(**arguments)

        with tf.control_dependencies(control_inputs=(loss_before,)):
            deltas = self.optimizer.step(
                time=time,
                variables=variables,
                arguments=arguments,
                fn_loss=fn_loss,
                return_estimated_improvement=True,
                **kwargs
            )

            if isinstance(deltas, tuple):
                # If 'return_estimated_improvement' argument exists.
                if len(deltas) != 2:
                    raise TensorForceError("Unexpected output of internal optimizer.")
                deltas, estimated_improvement = deltas
                # Negative value since line search maximizes.
                estimated_improvement = -estimated_improvement
            else:
                estimated_improvement = None

        with tf.control_dependencies(control_inputs=deltas):
                # Negative value since line search maximizes.
            loss_step = -fn_loss(**arguments)

        with tf.control_dependencies(control_inputs=(loss_step,)):

            def evaluate_step(deltas):
                with tf.control_dependencies(control_inputs=deltas):
                    applied = self.apply_step(variables=variables, deltas=deltas)
                with tf.control_dependencies(control_inputs=(applied,)):
                    # Negative value since line search maximizes.
                    return -fn_loss(**arguments)

            return self.solver.solve(
                fn_x=evaluate_step,
                x_init=deltas,
                base_value=loss_before,
                target_value=loss_step,
                estimated_improvement=estimated_improvement
            )