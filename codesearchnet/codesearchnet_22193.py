def covar(self):
        """
        The covariance matrix for the result :math:`\\beta`
        """
        if self._covar is None:
            self._covar = _np.linalg.inv(_np.dot(_np.transpose(self.X), self.X))
        return self._covar