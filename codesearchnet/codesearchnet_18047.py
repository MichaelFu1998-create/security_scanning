def update_Broyden_J(self):
        """Execute a Broyden update of J"""
        CLOG.debug('Broyden update.')
        delta_vals = self.param_vals - self._last_vals
        delta_residuals = self.calc_residuals() - self._last_residuals
        nrm = np.sqrt(np.dot(delta_vals, delta_vals))
        direction = delta_vals / nrm
        vals = delta_residuals / nrm
        self._rank_1_J_update(direction, vals)
        self.JTJ = np.dot(self.J, self.J.T)