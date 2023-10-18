def tf_step(self, time, variables, **kwargs):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            **kwargs: Additional arguments passed on to the internal optimizer.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """
        deltas = self.optimizer.step(time=time, variables=variables, **kwargs)

        with tf.control_dependencies(control_inputs=deltas):
            clipped_deltas = list()
            exceeding_deltas = list()
            for delta in deltas:
                clipped_delta = tf.clip_by_value(
                    t=delta,
                    clip_value_min=-self.clipping_value,
                    clip_value_max=self.clipping_value
                )
                clipped_deltas.append(clipped_delta)
                exceeding_deltas.append(clipped_delta - delta)

        applied = self.apply_step(variables=variables, deltas=exceeding_deltas)

        with tf.control_dependencies(control_inputs=(applied,)):
            return [delta + 0.0 for delta in clipped_deltas]