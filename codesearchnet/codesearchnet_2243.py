def minimize(self, time, variables, **kwargs):
        """
        Performs an optimization step.

        Args:
            time: Time tensor. Not used for this
            variables: List of variables to optimize.
            **kwargs: 
                fn_loss : loss function tensor that is differentiated
                sampled_loss : the sampled loss from running the model.

        Returns:
            The optimization operation.
        """
        loss = kwargs["fn_loss"]
        sampled_loss = kwargs["sampled_loss"]

        min_op, _ = self.minimize_(loss, sampled_loss, var_list=variables)
        return min_op