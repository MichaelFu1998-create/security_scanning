def dist(self, src, tar, diff_lens=True):
        """Return the normalized Hamming distance between two strings.

        Hamming distance normalized to the interval [0, 1].

        The Hamming distance is normalized by dividing it
        by the greater of the number of characters in src & tar (unless
        diff_lens is set to False, in which case an exception is raised).

        The arguments are identical to those of the hamming() function.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        diff_lens : bool
            If True (default), this returns the Hamming distance for those
            characters that have a matching character in both strings plus the
            difference in the strings' lengths. This is equivalent to extending
            the shorter string with obligatorily non-matching characters. If
            False, an exception is raised in the case of strings of unequal
            lengths.

        Returns
        -------
        float
            Normalized Hamming distance

        Examples
        --------
        >>> cmp = Hamming()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar, diff_lens) / max(len(src), len(tar))