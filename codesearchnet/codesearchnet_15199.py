def fit(self, verbose=True):
        """
        Maximise the marginal likelihood.

        Parameters
        ----------
        verbose : bool, optional
            ``True`` for progress output; ``False`` otherwise.
            Defaults to ``True``.
        """
        if not self._isfixed("logistic"):
            self._maximize_scalar(desc="LMM", rtol=1e-6, atol=1e-6, verbose=verbose)

        if not self._fix["beta"]:
            self._update_beta()

        if not self._fix["scale"]:
            self._update_scale()