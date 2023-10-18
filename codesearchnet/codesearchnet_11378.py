def _ends_in_cvc(self, term):
        """Return Porter helper function _ends_in_cvc value.

        Parameters
        ----------
        term : str
            The word to scan for cvc

        Returns
        -------
        bool
            True iff the stem ends in cvc (as defined in the Porter stemmer
            definition)

        """
        return len(term) > 2 and (
            term[-1] not in self._vowels
            and term[-2] in self._vowels
            and term[-3] not in self._vowels
            and term[-1] not in tuple('wxY')
        )