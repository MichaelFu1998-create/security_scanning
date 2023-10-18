def calc_grad(self):
        """The gradient of the cost w.r.t. the parameters."""
        residuals = self.calc_residuals()
        return 2*np.dot(self.J, residuals)