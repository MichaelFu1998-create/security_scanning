def scan(self, A1, X1):
        """
        LML, fixed-effect sizes, and scale of the candidate set.

        Parameters
        ----------
        A1 : (p, e) array_like
            Trait-by-environments design matrix.
        X1 : (n, m) array_like
            Variants set matrix.

        Returns
        -------
        lml : float
            Log of the marginal likelihood for the set.
        effsizes0 : (c, p) ndarray
            Fixed-effect sizes for the covariates.
        effsizes0_se : (c, p) ndarray
            Fixed-effect size standard errors for the covariates.
        effsizes1 : (m, e) ndarray
            Fixed-effect sizes for the candidates.
        effsizes1_se : (m, e) ndarray
            Fixed-effect size standard errors for the candidates.
        scale : float
            Optimal scale.
        """
        from numpy import empty
        from numpy.linalg import multi_dot
        from numpy_sugar import epsilon, is_all_finite
        from scipy.linalg import cho_solve

        A1 = asarray(A1, float)
        X1 = asarray(X1, float)

        if not is_all_finite(A1):
            raise ValueError("A1 parameter has non-finite elements.")

        if not is_all_finite(X1):
            raise ValueError("X1 parameter has non-finite elements.")

        if A1.shape[1] == 0:
            beta_se = sqrt(self.null_beta_covariance.diagonal())
            return {
                "lml": self.null_lml(),
                "effsizes0": unvec(self.null_beta, (self._ncovariates, -1)),
                "effsizes0_se": unvec(beta_se, (self._ncovariates, -1)),
                "effsizes1": empty((0,)),
                "effsizes1_se": empty((0,)),
                "scale": self.null_scale,
            }

        X1X1 = X1.T @ X1
        XX1 = self._X.T @ X1
        AWA1 = self._WA.T @ A1
        A1W = A1.T @ self._W
        GX1 = self._G.T @ X1

        MRiM1 = kron(AWA1, XX1)
        M1RiM1 = kron(A1W @ A1, X1X1)

        M1Riy = vec(multi_dot([X1.T, self._Y, A1W.T]))
        XRiM1 = kron(self._WL0.T @ A1, GX1)
        ZiXRiM1 = cho_solve(self._Lz, XRiM1)

        MRiXZiXRiM1 = self._XRiM.T @ ZiXRiM1
        M1RiXZiXRiM1 = XRiM1.T @ ZiXRiM1
        M1RiXZiXRiy = XRiM1.T @ self._ZiXRiy

        T0 = [[self._MRiM, MRiM1], [MRiM1.T, M1RiM1]]
        T1 = [[self._MRiXZiXRiM, MRiXZiXRiM1], [MRiXZiXRiM1.T, M1RiXZiXRiM1]]
        T2 = [self._MRiy, M1Riy]
        T3 = [self._MRiXZiXRiy, M1RiXZiXRiy]

        MKiM = block(T0) - block(T1)
        MKiy = block(T2) - block(T3)
        beta = rsolve(MKiM, MKiy)

        mKiy = beta.T @ MKiy
        cp = self._ntraits * self._ncovariates
        effsizes0 = unvec(beta[:cp], (self._ncovariates, self._ntraits))
        effsizes1 = unvec(beta[cp:], (X1.shape[1], A1.shape[1]))

        np = self._nsamples * self._ntraits
        sqrtdot = self._yKiy - mKiy
        scale = clip(sqrtdot / np, epsilon.tiny, inf)
        lml = self._static_lml() / 2 - np * safe_log(scale) / 2 - np / 2

        effsizes_se = sqrt(clip(scale * pinv(MKiM).diagonal(), epsilon.tiny, inf))
        effsizes0_se = unvec(effsizes_se[:cp], (self._ncovariates, self._ntraits))
        effsizes1_se = unvec(effsizes_se[cp:], (X1.shape[1], A1.shape[1]))

        return {
            "lml": lml,
            "effsizes0": effsizes0,
            "effsizes1": effsizes1,
            "scale": scale,
            "effsizes0_se": effsizes0_se,
            "effsizes1_se": effsizes1_se,
        }