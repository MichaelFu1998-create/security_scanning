def _cond_n(self, word, suffix_len):
        """Return Lovins' condition N.

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
        if len(word) - suffix_len >= 3:
            if word[-suffix_len - 3] == 's':
                if len(word) - suffix_len >= 4:
                    return True
            else:
                return True
        return False