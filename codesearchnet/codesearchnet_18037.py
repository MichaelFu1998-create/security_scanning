def update_param_vals(self, new_vals, incremental=False):
        """
        Updates the current set of parameter values and previous values,
        sets a flag to re-calculate J.

        Parameters
        ----------
            new_vals : numpy.ndarray
                The new values to update to
            incremental : Bool, optional
                Set to True to make it an incremental update relative
                to the old parameters. Default is False
        """
        self._last_vals = self.param_vals.copy()
        if incremental:
            self.param_vals += new_vals
        else:
            self.param_vals = new_vals.copy()
        #And we've updated, so JTJ is no longer valid:
        self._fresh_JTJ = False