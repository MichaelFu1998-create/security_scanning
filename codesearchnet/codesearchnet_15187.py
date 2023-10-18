def posteriori_mean(self):
        r""" Mean of the estimated posteriori.

        This is also the maximum a posteriori estimation of the latent variable.
        """
        from numpy_sugar.linalg import rsolve

        Sigma = self.posteriori_covariance()
        eta = self._ep._posterior.eta
        return dot(Sigma, eta + rsolve(GLMM.covariance(self), self.mean()))