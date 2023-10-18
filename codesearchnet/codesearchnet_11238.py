def _sb_has_vowel(self, term):
        """Return Porter helper function _sb_has_vowel value.

        Parameters
        ----------
        term : str
            The term to examine

        Returns
        -------
        bool
            True iff a vowel exists in the term (as defined in the Porter
            stemmer definition)

        """
        for letter in term:
            if letter in self._vowels:
                return True
        return False