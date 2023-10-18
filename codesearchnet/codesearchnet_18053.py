def update_function(self, param_vals):
        """Takes an array param_vals, updates function, returns the new error"""
        self.model = self.func(param_vals, *self.func_args, **self.func_kwargs)
        d = self.calc_residuals()
        return np.dot(d.flat, d.flat)