def beta(self):
        """
        The result :math:`\\beta` of the linear least squares
        """
        if self._beta is None:
            # This is the linear least squares matrix formalism
            self._beta = _np.dot(_np.linalg.pinv(self.X) , self.y)
        return self._beta