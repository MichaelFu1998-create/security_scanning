def update_function(self, param_vals):
        """Updates the opt_obj, returns new error."""
        self.opt_obj.update_function(param_vals)
        return self.opt_obj.get_error()