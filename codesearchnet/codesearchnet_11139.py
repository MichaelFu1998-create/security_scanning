def sim(self, src, tar):
        """Return the prefix similarity of two strings.

        Prefix similarity is the ratio of the length of the shorter term that
        exactly matches the longer term to the length of the shorter term,
        beginning at the start of both terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Prefix similarity

        Examples
        --------
        >>> cmp = Prefix()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.25
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
        min_len = len(min_word)
        for i in range(min_len, 0, -1):
            if min_word[:i] == max_word[:i]:
                return i / min_len
        return 0.0