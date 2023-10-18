def gradient(self):
        """
        Derivative of the covariance matrix over the parameters of L.

        Returns
        -------
        Lu : ndarray
            Derivative of K over the lower triangular part of L.
        """
        L = self.L
        self._grad_Lu[:] = 0

        for i in range(len(self._tril1[0])):
            row = self._tril1[0][i]
            col = self._tril1[1][i]
            self._grad_Lu[row, :, i] = L[:, col]
            self._grad_Lu[:, row, i] += L[:, col]

        m = len(self._tril1[0])
        for i in range(len(self._diag[0])):
            row = self._diag[0][i]
            col = self._diag[1][i]
            self._grad_Lu[row, :, m + i] = L[row, col] * L[:, col]
            self._grad_Lu[:, row, m + i] += L[row, col] * L[:, col]

        return {"Lu": self._grad_Lu}