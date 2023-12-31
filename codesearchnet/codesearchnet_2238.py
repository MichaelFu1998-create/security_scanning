def tf_step(
        self,
        time,
        variables,
        arguments,
        fn_loss,
        **kwargs
    ):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            arguments: Dict of arguments for callables, like fn_loss.
            fn_loss: A callable returning the loss of the current model.
            **kwargs: Additional arguments, not used.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """
        unperturbed_loss = fn_loss(**arguments)

        # First sample
        perturbations = [tf.random_normal(shape=util.shape(variable)) * self.learning_rate for variable in variables]
        applied = self.apply_step(variables=variables, deltas=perturbations)

        with tf.control_dependencies(control_inputs=(applied,)):
            perturbed_loss = fn_loss(**arguments)
            direction = tf.sign(x=(unperturbed_loss - perturbed_loss))
            deltas_sum = [direction * perturbation for perturbation in perturbations]

        if self.unroll_loop:
            # Unrolled for loop
            previous_perturbations = perturbations
            for sample in xrange(self.num_samples):

                with tf.control_dependencies(control_inputs=deltas_sum):
                    perturbations = [tf.random_normal(shape=util.shape(variable)) * self.learning_rate for variable in variables]
                    perturbation_deltas = [
                        pert - prev_pert for pert, prev_pert in zip(perturbations, previous_perturbations)
                    ]
                    applied = self.apply_step(variables=variables, deltas=perturbation_deltas)
                    previous_perturbations = perturbations

                with tf.control_dependencies(control_inputs=(applied,)):
                    perturbed_loss = fn_loss(**arguments)
                    direction = tf.sign(x=(unperturbed_loss - perturbed_loss))
                    deltas_sum = [delta + direction * perturbation for delta, perturbation in zip(deltas_sum, perturbations)]

        else:
            # TensorFlow while loop
            def body(iteration, deltas_sum, previous_perturbations):

                with tf.control_dependencies(control_inputs=deltas_sum):
                    perturbations = [tf.random_normal(shape=util.shape(variable)) * self.learning_rate for variable in variables]
                    perturbation_deltas = [
                        pert - prev_pert for pert, prev_pert in zip(perturbations, previous_perturbations)
                    ]
                    applied = self.apply_step(variables=variables, deltas=perturbation_deltas)

                with tf.control_dependencies(control_inputs=(applied,)):
                    perturbed_loss = fn_loss(**arguments)
                    direction = tf.sign(x=(unperturbed_loss - perturbed_loss))
                    deltas_sum = [delta + direction * perturbation for delta, perturbation in zip(deltas_sum, perturbations)]

                return iteration + 1, deltas_sum, perturbations

            def cond(iteration, deltas_sum, previous_perturbation):
                return iteration < self.num_samples - 1

            _, deltas_sum, perturbations = tf.while_loop(cond=cond, body=body, loop_vars=(0, deltas_sum, perturbations))

        with tf.control_dependencies(control_inputs=deltas_sum):
            deltas = [delta / self.num_samples for delta in deltas_sum]
            perturbation_deltas = [delta - pert for delta, pert in zip(deltas, perturbations)]
            applied = self.apply_step(variables=variables, deltas=perturbation_deltas)

        with tf.control_dependencies(control_inputs=(applied,)):
            # Trivial operation to enforce control dependency
            return [delta + 0.0 for delta in deltas]