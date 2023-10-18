def scan(self, M):
        """
        LML, fixed-effect sizes, and scale of the candidate set.

        Parameters
        ----------
        M : array_like
            Fixed-effects set.

        Returns
        -------
        lml : float
            Log of the marginal likelihood.
        effsizes0 : ndarray
            Covariates fixed-effect sizes.
        effsizes0_se : ndarray
            Covariates fixed-effect size standard errors.
        effsizes1 : ndarray
            Candidate set fixed-effect sizes.
        effsizes1_se : ndarray
            Candidate fixed-effect size standard errors.
        scale : ndarray
            Optimal scale.
        """
        from numpy_sugar.linalg import ddot
        from numpy_sugar import is_all_finite

        M = asarray(M, float)

        if M.shape[1] == 0:
            return {
                "lml": self.null_lml(),
                "effsizes0": self.null_beta,
                "effsizes0_se": self.null_beta_se,
                "effsizes1": empty((0)),
                "effsizes1_se": empty((0)),
                "scale": self.null_scale,
            }

        if not is_all_finite(M):
            raise ValueError("M parameter has non-finite elements.")

        MTQ = [dot(M.T, Q) for Q in self._QS[0] if Q.size > 0]
        yTBM = [dot(i, j.T) for (i, j) in zip(self._yTQDi, MTQ)]
        XTBM = [dot(i, j.T) for (i, j) in zip(self._XTQDi, MTQ)]
        D = self._D
        MTBM = [ddot(i, 1 / j) @ i.T for i, j in zip(MTQ, D) if j.min() > 0]

        return self._multicovariate_set(yTBM, XTBM, MTBM)