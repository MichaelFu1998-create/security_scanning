def sim(self, src, tar):
        """Return the length similarity of two strings.

        Length similarity is the ratio of the length of the shorter string to
        the longer.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Length similarity

        Examples
        --------
        >>> cmp = Length()
        >>> cmp.sim('cat', 'hat')
        1.0
        >>> cmp.sim('Niall', 'Neil')
        0.8
        >>> cmp.sim('aluminum', 'Catalan')
        0.875
        >>> cmp.sim('ATCG', 'TAGC')
        1.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        return (
            len(src) / len(tar) if len(src) < len(tar) else len(tar) / len(src)
        )