def get_variables(self, include_submodules=False, include_nontrainable=False):
        """
        Returns the TensorFlow variables used by the model.

        Args:
            include_submodules: Includes variables of submodules (e.g. baseline, target network)
                if true.
            include_nontrainable: Includes non-trainable variables if true.

        Returns:
            List of variables.
        """
        if include_nontrainable:
            model_variables = [self.all_variables[key] for key in sorted(self.all_variables)]

            states_preprocessing_variables = [
                variable for name in sorted(self.states_preprocessing)
                for variable in self.states_preprocessing[name].get_variables()
            ]
            model_variables += states_preprocessing_variables

            actions_exploration_variables = [
                variable for name in sorted(self.actions_exploration)
                for variable in self.actions_exploration[name].get_variables()
            ]
            model_variables += actions_exploration_variables

            if self.reward_preprocessing is not None:
                reward_preprocessing_variables = self.reward_preprocessing.get_variables()
                model_variables += reward_preprocessing_variables

        else:
            model_variables = [self.variables[key] for key in sorted(self.variables)]

        return model_variables