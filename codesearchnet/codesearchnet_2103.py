def apply_step(self, variables, deltas):
        """
        Applies the given (and already calculated) step deltas to the variable values.

        Args:
            variables: List of variables.
            deltas: List of deltas of same length.

        Returns:
            The step-applied operation. A tf.group of tf.assign_add ops.
        """
        if len(variables) != len(deltas):
            raise TensorForceError("Invalid variables and deltas lists.")
        return tf.group(
            *(tf.assign_add(ref=variable, value=delta) for variable, delta in zip(variables, deltas))
        )