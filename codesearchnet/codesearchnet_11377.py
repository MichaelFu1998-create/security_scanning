def _ends_in_doubled_cons(self, term):
        """Return Porter helper function _ends_in_doubled_cons value.

        Parameters
        ----------
        term : str
            The word to check for a final doubled consonant

        Returns
        -------
        bool
            True iff the stem ends in a doubled consonant (as defined in the
            Porter stemmer definition)

        """
        return (
            len(term) > 1
            and term[-1] not in self._vowels
            and term[-2] == term[-1]
        )