def get_variables(self, include_submodules=False, include_nontrainable=False):
        """
        Returns the TensorFlow variables used by the model.

        Returns:
            List of variables.
        """
        model_variables = super(QDemoModel, self).get_variables(
            include_submodules=include_submodules,
            include_nontrainable=include_nontrainable
        )

        if include_nontrainable:
            demo_memory_variables = self.demo_memory.get_variables()
            model_variables += demo_memory_variables

        return model_variables