def _cond_k(self, word, suffix_len):
        """Return Lovins' condition K.

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
        return (len(word) - suffix_len >= 3) and (
            word[-suffix_len - 1] in {'i', 'l'}
            or (word[-suffix_len - 3] == 'u' and word[-suffix_len - 1] == 'e')
        )