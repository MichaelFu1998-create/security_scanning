def _set_err_paramvals(self):
        """
        Must update:
            self.error, self._last_error, self.param_vals, self._last_vals
        """
        # self.param_vals = p0 #sloppy...
        self._last_vals = self.param_vals.copy()
        self.error = self.update_function(self.param_vals)
        self._last_error = (1 + 2*self.fractol) * self.error