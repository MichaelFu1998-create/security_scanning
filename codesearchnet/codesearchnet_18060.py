def calc_grad(self):
        """The gradient of the cost w.r.t. the parameters."""
        if self._fresh_JTJ:
            return self._graderr
        else:
            residuals = self.calc_residuals()
            return 2*np.dot(self.J, residuals)