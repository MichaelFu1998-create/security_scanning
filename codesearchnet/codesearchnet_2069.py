def get_variables(self, include_nontrainable=False):
        """
        Returns the TensorFlow variables used by the baseline.

        Returns:
            List of variables
        """
        if include_nontrainable:
            return [self.all_variables[key] for key in sorted(self.all_variables)]
        else:
            return [self.variables[key] for key in sorted(self.variables)]