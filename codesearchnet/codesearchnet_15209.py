def L(self):
        r"""Cholesky decomposition of :math:`\mathrm B`.

        .. math::

            \mathrm B = \mathrm Q^{\intercal}\tilde{\mathrm{T}}\mathrm Q
                + \mathrm{S}^{-1}
        """
        from scipy.linalg import cho_factor
        from numpy_sugar.linalg import ddot, sum2diag

        if self._L_cache is not None:
            return self._L_cache

        Q = self._cov["QS"][0][0]
        S = self._cov["QS"][1]
        B = dot(Q.T, ddot(self._site.tau, Q, left=True))
        sum2diag(B, 1.0 / S, out=B)
        self._L_cache = cho_factor(B, lower=True)[0]
        return self._L_cache