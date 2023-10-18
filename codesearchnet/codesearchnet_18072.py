def error(self):
        """
        Class property: Sum of the squared errors,
        :math:`E = \sum_i (D_i - M_i(\\theta))^2`
        """
        r = self.residuals.ravel()
        return np.dot(r,r)