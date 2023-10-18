def dist_abs(self, src, tar, diff_lens=True):
        """Return the Hamming distance between two strings.

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
        int
            The Hamming distance between src & tar

        Raises
        ------
        ValueError
            Undefined for sequences of unequal length; set diff_lens to True
            for Hamming distance between strings of unequal lengths.

        Examples
        --------
        >>> cmp = Hamming()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        8
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4

        """
        if not diff_lens and len(src) != len(tar):
            raise ValueError(
                'Undefined for sequences of unequal length; set diff_lens '
                + 'to True for Hamming distance between strings of unequal '
                + 'lengths.'
            )

        hdist = 0
        if diff_lens:
            hdist += abs(len(src) - len(tar))
        hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

        return hdist