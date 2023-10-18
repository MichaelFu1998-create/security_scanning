def baseline_optimizer_arguments(self, states, internals, reward):
        """
        Returns the baseline optimizer arguments including the time, the list of variables to  
        optimize, and various functions which the optimizer might require to perform an update  
        step.

        Args:
            states: Dict of state tensors.
            internals: List of prior internal state tensors.
            reward: Reward tensor.

        Returns:
            Baseline optimizer arguments as dict.
        """
        arguments = dict(
            time=self.global_timestep,
            variables=self.baseline.get_variables(),
            arguments=dict(
                states=states,
                internals=internals,
                reward=reward,
                update=tf.constant(value=True),
            ),
            fn_reference=self.baseline.reference,
            fn_loss=self.fn_baseline_loss,
            # source_variables=self.network.get_variables()
        )
        if self.global_model is not None:
            arguments['global_variables'] = self.global_model.baseline.get_variables()
        return arguments