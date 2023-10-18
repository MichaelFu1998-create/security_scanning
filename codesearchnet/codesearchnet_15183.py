def L(self):
        r"""Cholesky decomposition of :math:`\mathrm B`.

        .. math::

            \mathrm B = \mathrm Q^{\intercal}\tilde{\mathrm{T}}\mathrm Q
                + \mathrm{S}^{-1}
        """
        from numpy_sugar.linalg import ddot, sum2diag

        if self._L_cache is not None:
            return self._L_cache

        s = self._cov["scale"]
        d = self._cov["delta"]
        Q = self._cov["QS"][0][0]
        S = self._cov["QS"][1]

        ddot(self.A * self._site.tau, Q, left=True, out=self._NxR)
        B = dot(Q.T, self._NxR, out=self._RxR)
        B *= 1 - d
        sum2diag(B, 1.0 / S / s, out=B)
        self._L_cache = _cho_factor(B)
        return self._L_cache