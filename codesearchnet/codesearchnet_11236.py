def _sb_ends_in_short_syllable(self, term):
        """Return True iff term ends in a short syllable.

        (...according to the Porter2 specification.)

        NB: This is akin to the CVC test from the Porter stemmer. The
        description is unfortunately poor/ambiguous.

        Parameters
        ----------
        term : str
            The term to examine

        Returns
        -------
        bool
            True iff term ends in a short syllable

        """
        if not term:
            return False
        if len(term) == 2:
            if term[-2] in self._vowels and term[-1] not in self._vowels:
                return True
        elif len(term) >= 3:
            if (
                term[-3] not in self._vowels
                and term[-2] in self._vowels
                and term[-1] in self._codanonvowels
            ):
                return True
        return False