def _initialize(self):
        r"""Initialize the mean and covariance of the posterior.

        Given that :math:`\tilde{\mathrm T}` is a matrix of zeros right before
        the first EP iteration, we have

        .. math::

            \boldsymbol\mu = \mathrm K^{-1} \mathbf m ~\text{ and }~
            \Sigma = \mathrm K

        as the initial posterior mean and covariance.
        """
        if self._mean is None or self._cov is None:
            return

        Q = self._cov["QS"][0][0]
        S = self._cov["QS"][1]

        if S.size > 0:
            self.tau[:] = 1 / npsum((Q * sqrt(S)) ** 2, axis=1)
        else:
            self.tau[:] = 0.0
        self.eta[:] = self._mean
        self.eta[:] *= self.tau