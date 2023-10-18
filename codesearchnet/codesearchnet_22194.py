def chisq_red(self):
        """
        The reduced chi-square of the linear least squares
        """
        if self._chisq_red is None:
            self._chisq_red = chisquare(self.y_unweighted.transpose(), _np.dot(self.X_unweighted, self.beta), self.y_error, ddof=3, verbose=False)
        return self._chisq_red