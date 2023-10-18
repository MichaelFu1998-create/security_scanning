def target_optimizer_arguments(self):
        """
        Returns the target optimizer arguments including the time, the list of variables to  
        optimize, and various functions which the optimizer might require to perform an update  
        step.

        Returns:
            Target optimizer arguments as dict.
        """
        variables = self.target_network.get_variables() + [
            variable for name in sorted(self.target_distributions)
            for variable in self.target_distributions[name].get_variables()
        ]
        source_variables = self.network.get_variables() + [
            variable for name in sorted(self.distributions)
            for variable in self.distributions[name].get_variables()
        ]
        arguments = dict(
            time=self.global_timestep,
            variables=variables,
            source_variables=source_variables
        )
        if self.global_model is not None:
            arguments['global_variables'] = self.global_model.target_network.get_variables() + [
                variable for name in sorted(self.global_model.target_distributions)
                for variable in self.global_model.target_distributions[name].get_variables()
            ]
        return arguments