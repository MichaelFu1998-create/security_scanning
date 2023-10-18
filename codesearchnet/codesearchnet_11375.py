def _m_degree(self, term):
        """Return Porter helper function _m_degree value.

        m-degree is equal to the number of V to C transitions

        Parameters
        ----------
        term : str
            The word for which to calculate the m-degree

        Returns
        -------
        int
            The m-degree as defined in the Porter stemmer definition

        """
        mdeg = 0
        last_was_vowel = False
        for letter in term:
            if letter in self._vowels:
                last_was_vowel = True
            else:
                if last_was_vowel:
                    mdeg += 1
                last_was_vowel = False
        return mdeg