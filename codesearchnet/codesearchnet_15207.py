def value(self):
        r"""Log of the marginal likelihood.

        Formally,

        .. math::

            - \frac{n}{2}\log{2\pi} - \frac{1}{2} \log{\left|
                v_0 \mathrm K + v_1 \mathrm I + \tilde{\Sigma} \right|}
                    - \frac{1}{2}
                    \left(\tilde{\boldsymbol\mu} -
                    \mathrm X\boldsymbol\beta\right)^{\intercal}
                    \left( v_0 \mathrm K + v_1 \mathrm I +
                    \tilde{\Sigma} \right)^{-1}
                    \left(\tilde{\boldsymbol\mu} -
                    \mathrm X\boldsymbol\beta\right)

        Returns
        -------
        float
            :math:`\log{p(\tilde{\boldsymbol\mu})}`
        """
        from numpy_sugar.linalg import ddot, sum2diag

        if self._cache["value"] is not None:
            return self._cache["value"]

        scale = exp(self.logscale)
        delta = 1 / (1 + exp(-self.logitdelta))

        v0 = scale * (1 - delta)
        v1 = scale * delta

        mu = self.eta / self.tau
        n = len(mu)
        if self._QS is None:
            K = zeros((n, n))
        else:
            Q0 = self._QS[0][0]
            S0 = self._QS[1]
            K = dot(ddot(Q0, S0), Q0.T)

        A = sum2diag(sum2diag(v0 * K, v1), 1 / self.tau)
        m = mu - self.mean()

        v = -n * log(2 * pi)
        v -= slogdet(A)[1]
        v -= dot(m, solve(A, m))

        self._cache["value"] = v / 2

        return self._cache["value"]