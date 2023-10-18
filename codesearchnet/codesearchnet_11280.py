def _undouble(self, word):
        """Undouble endings -kk, -dd, and -tt.

        Parameters
        ----------
        word : str
          The word to stem

        Returns
        -------
        str
            The word with doubled endings undoubled

        """
        if (
            len(word) > 1
            and word[-1] == word[-2]
            and word[-1] in {'d', 'k', 't'}
        ):
            return word[:-1]
        return word