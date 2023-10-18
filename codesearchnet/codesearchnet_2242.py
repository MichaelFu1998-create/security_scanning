def apply_step(self, variables, deltas, loss_sampled):
        """
        Applies the given (and already calculated) step deltas to the variable values.

        Args:
            variables: List of variables.
            deltas: List of deltas of same length.
            loss_sampled : the sampled loss

        Returns:
            The step-applied operation. A tf.group of tf.assign_add ops.
        """
        update_stats_op = self.compute_and_apply_stats(
            loss_sampled, var_list=var_list)
        grads = [(a, b) for a, b in zip(deltas, varlist)]
        kfacOptim, _ = self.apply_gradients_kfac(grads)
        return kfacOptim