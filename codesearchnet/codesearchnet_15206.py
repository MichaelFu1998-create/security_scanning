def get_fast_scanner(self):
        r"""Return :class:`glimix_core.lmm.FastScanner` for the current
        delta."""
        from numpy_sugar.linalg import ddot, economic_qs, sum2diag

        y = self.eta / self.tau

        if self._QS is None:
            K = eye(y.shape[0]) / self.tau
        else:
            Q0 = self._QS[0][0]
            S0 = self._QS[1]
            K = dot(ddot(Q0, self.v0 * S0), Q0.T)
            K = sum2diag(K, 1 / self.tau)

        return FastScanner(y, self._X, economic_qs(K), self.v1)