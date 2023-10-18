def optimizer_arguments(self, states, internals, actions, terminal, reward, next_states, next_internals):
        """
        Returns the optimizer arguments including the time, the list of variables to optimize,
        and various functions which the optimizer might require to perform an update step.

        Args:
            states (dict): Dict of state tensors.
            internals (dict): Dict of prior internal state tensors.
            actions (dict): Dict of action tensors.
            terminal: 1D boolean is-terminal tensor.
            reward: 1D (float) rewards tensor.
            next_states (dict): Dict of successor state tensors.
            next_internals (dict): Dict of posterior internal state tensors.

        Returns:
            Optimizer arguments as dict to be used as **kwargs to the optimizer.
        """
        arguments = dict(
            time=self.global_timestep,
            variables=self.get_variables(),
            arguments=dict(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward,
                next_states=next_states,
                next_internals=next_internals,
                update=tf.constant(value=True)
            ),
            fn_reference=self.fn_reference,
            fn_loss=self.fn_loss
        )
        if self.global_model is not None:
            arguments['global_variables'] = self.global_model.get_variables()
        return arguments