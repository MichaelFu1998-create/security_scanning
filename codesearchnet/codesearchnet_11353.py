def _cond_s(self, word, suffix_len):
        """Return Lovins' condition S.

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
        return word[-suffix_len - 2 : -suffix_len] == 'dr' or (
            word[-suffix_len - 1] == 't'
            and word[-suffix_len - 2 : -suffix_len] != 'tt'
        )