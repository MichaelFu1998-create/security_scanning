def y(self):
        """
        The :math:`X` weighted properly by the errors from *y_error*
        """
        if self._y is None:
            self._y = self.y_unweighted/self.y_error
        return self._y