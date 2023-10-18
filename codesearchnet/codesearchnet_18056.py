def calc_J(self):
        """Calculates J along the direction."""
        r0 = self.state.residuals.copy().ravel()
        dl = np.zeros(self.param_vals.size)
        p0 = self.param_vals.copy()
        J = []
        for a in range(self.param_vals.size):
            dl *= 0
            dl[a] += self.dl
            self.update_function(p0 + dl)
            r1 = self.state.residuals.copy().ravel()
            J.append( (r1-r0)/self.dl)
        self.update_function(p0)
        return np.array(J)