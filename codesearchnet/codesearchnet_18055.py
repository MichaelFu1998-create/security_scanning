def update_function(self, param_vals):
        """Updates with param_vals[i] = distance from self.p0 along self.direction[i]."""
        dp = np.zeros(self.p0.size)
        for a in range(param_vals.size):
            dp += param_vals[a] * self.directions[a]
        self.state.update(self.state.params, self.p0 + dp)
        self.param_vals[:] = param_vals
        return None