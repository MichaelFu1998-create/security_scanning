def posteriori_covariance(self):
        r""" Covariance of the estimated posteriori."""
        K = GLMM.covariance(self)
        tau = self._ep._posterior.tau
        return pinv(pinv(K) + diag(1 / tau))