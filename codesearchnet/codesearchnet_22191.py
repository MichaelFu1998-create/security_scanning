def y_fit(self):
        """
        Using the result of the linear least squares, the result of :math:`X_{ij}\\beta_i`
        """
        if self._y_fit is None:
            self._y_fit = _np.dot(self.X_unweighted, self.beta)
        return self._y_fit