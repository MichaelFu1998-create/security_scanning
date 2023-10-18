def fit(self, verbose=True, factr=1e5, pgtol=1e-7):
        r"""Maximise the marginal likelihood.

        Parameters
        ----------
        verbose : bool
            ``True`` for progress output; ``False`` otherwise.
            Defaults to ``True``.
        factr : float, optional
            The iteration stops when
            ``(f^k - f^{k+1})/max{|f^k|,|f^{k+1}|,1} <= factr * eps``, where ``eps`` is
            the machine precision.
        pgtol : float, optional
            The iteration will stop when ``max{|proj g_i | i = 1, ..., n} <= pgtol``
            where ``pg_i`` is the i-th component of the projected gradient.

        Notes
        -----
        Please, refer to :func:`scipy.optimize.fmin_l_bfgs_b` for further information
        about ``factr`` and ``pgtol``.
        """
        self._maximize(verbose=verbose, factr=factr, pgtol=pgtol)