def _cond_x(self, word, suffix_len):
        """Return Lovins' condition X.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'i', 'l'} or (
            word[-suffix_len - 3 : -suffix_len] == 'u'
            and word[-suffix_len - 1] == 'e'
        )