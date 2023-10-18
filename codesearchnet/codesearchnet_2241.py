def tf_step(self, time, variables, **kwargs):
        """
        Creates the TensorFlow operations for performing an optimization step on the given variables, including
        actually changing the values of the variables.

        Args:
            time: Time tensor. Not used for this optimizer.
            variables: List of variables to optimize.
            **kwargs: 
                fn_loss : loss function tensor to differentiate.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """
        fn_loss = kwargs["fn_loss"]
        if variables is None:
            variables = tf.trainable_variables
        return tf.gradients(fn_loss, variables)