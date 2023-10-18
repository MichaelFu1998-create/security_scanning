def get_fast_scanner(self):
        """
        Return :class:`.FastScanner` for association scan.

        Returns
        -------
        :class:`.FastScanner`
            Instance of a class designed to perform very fast association scan.
        """
        terms = self._terms
        return KronFastScanner(self._Y, self._mean.A, self._mean.X, self._cov.Ge, terms)