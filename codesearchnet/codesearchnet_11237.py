def _sb_short_word(self, term, r1_prefixes=None):
        """Return True iff term is a short word.

        (...according to the Porter2 specification.)

        Parameters
        ----------
        term : str
            The term to examine
        r1_prefixes : set
            Prefixes to consider

        Returns
        -------
        bool
            True iff term is a short word

        """
        if self._sb_r1(term, r1_prefixes) == len(
            term
        ) and self._sb_ends_in_short_syllable(term):
            return True
        return False