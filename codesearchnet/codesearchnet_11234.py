def _sb_r1(self, term, r1_prefixes=None):
        """Return the R1 region, as defined in the Porter2 specification.

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
        vowel_found = False
        if hasattr(r1_prefixes, '__iter__'):
            for prefix in r1_prefixes:
                if term[: len(prefix)] == prefix:
                    return len(prefix)

        for i in range(len(term)):
            if not vowel_found and term[i] in self._vowels:
                vowel_found = True
            elif vowel_found and term[i] not in self._vowels:
                return i + 1
        return len(term)