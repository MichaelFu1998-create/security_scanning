def dist_abs(self, src, tar):
        """Return the bag distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0
        >>> cmp.dist_abs('abcdefg', 'hijklm')
        7
        >>> cmp.dist_abs('abcdefg', 'hijklmno')
        8

        """
        if tar == src:
            return 0
        elif not src:
            return len(tar)
        elif not tar:
            return len(src)

        src_bag = Counter(src)
        tar_bag = Counter(tar)
        return max(
            sum((src_bag - tar_bag).values()),
            sum((tar_bag - src_bag).values()),
        )