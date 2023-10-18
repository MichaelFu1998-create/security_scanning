def _cond_bb(self, word, suffix_len):
        """Return Lovins' condition BB.

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
        return (
            len(word) - suffix_len >= 3
            and word[-suffix_len - 3 : -suffix_len] != 'met'
            and word[-suffix_len - 4 : -suffix_len] != 'ryst'
        )