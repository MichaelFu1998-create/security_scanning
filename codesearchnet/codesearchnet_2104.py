def minimize(self, time, variables, **kwargs):
        """
        Performs an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            **kwargs: Additional optimizer-specific arguments. The following arguments are used
                by some optimizers:
            - arguments: Dict of arguments for callables, like fn_loss.
            - fn_loss: A callable returning the loss of the current model.
            - fn_reference: A callable returning the reference values, in case of a comparative  
                loss.
            - fn_kl_divergence: A callable returning the KL-divergence relative to the
                current model.
            - sampled_loss: A sampled loss (integer).
            - return_estimated_improvement: Returns the estimated improvement resulting from
                the natural gradient calculation if true.
            - source_variables: List of source variables to synchronize with.
            - global_variables: List of global variables to apply the proposed optimization
                step to.


        Returns:
            The optimization operation.
        """
        # # Add training variable gradient histograms/scalars to summary output
        # # if 'gradients' in self.summary_labels:
        # if any(k in self.summary_labels for k in ['gradients', 'gradients_histogram', 'gradients_scalar']):
        #     valid = True
        #     if isinstance(self, tensorforce.core.optimizers.TFOptimizer):
        #         gradients = self.optimizer.compute_gradients(kwargs['fn_loss']())
        #     elif isinstance(self.optimizer, tensorforce.core.optimizers.TFOptimizer):
        #         # This section handles "Multi_step" and may handle others
        #         # if failure is found, add another elif to handle that case
        #         gradients = self.optimizer.optimizer.compute_gradients(kwargs['fn_loss']())
        #     else:
        #         # Didn't find proper gradient information
        #         valid = False

        #     # Valid gradient data found, create summary data items
        #     if valid:
        #         for grad, var in gradients:
        #             if grad is not None:
        #                 if any(k in self.summary_labels for k in ('gradients', 'gradients_scalar')):
        #                     axes = list(range(len(grad.shape)))
        #                     mean, var = tf.nn.moments(grad, axes)
        #                     tf.contrib.summary.scalar(name='gradients/' + var.name + "/mean", tensor=mean)
        #                     tf.contrib.summary.scalar(name='gradients/' + var.name + "/variance", tensor=var)
        #                 if any(k in self.summary_labels for k in ('gradients', 'gradients_histogram')):
        #                     tf.contrib.summary.histogram(name='gradients/' + var.name, tensor=grad)

        deltas = self.step(time=time, variables=variables, **kwargs)
        with tf.control_dependencies(control_inputs=deltas):
            return tf.no_op()