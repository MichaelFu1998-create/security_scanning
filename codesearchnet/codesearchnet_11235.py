def _sb_r2(self, term, r1_prefixes=None):
        """Return the R2 region, as defined in the Porter2 specification.

        Parameters
        ----------
        term : str
            The term to examine
        r1_prefixes : set
            Prefixes to consider

        Returns
        -------
        int
            Length of the R1 region

        """
        r1_start = self._sb_r1(term, r1_prefixes)
        return r1_start + self._sb_r1(term[r1_start:])