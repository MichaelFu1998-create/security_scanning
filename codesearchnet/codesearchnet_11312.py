def dist(self, src, tar, cost=(0, 1, 2), local=False):
        """Return the normalized Editex distance between two strings.

        The Editex distance is normalized by dividing the Editex distance
        (calculated by any of the three supported methods) by the greater of
        the number of characters in src times the cost of a delete and
        the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        cost : tuple
            A 3-tuple representing the cost of the four possible edits: match,
            same-group, and mismatch respectively (by default: (0, 1, 2))
        local : bool
            If True, the local variant of Editex is used

        Returns
        -------
        int
            Normalized Editex distance

        Examples
        --------
        >>> cmp = Editex()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.2
        >>> cmp.dist('aluminum', 'Catalan')
        0.75
        >>> cmp.dist('ATCG', 'TAGC')
        0.75

        """
        if src == tar:
            return 0.0
        mismatch_cost = cost[2]
        return self.dist_abs(src, tar, cost, local) / (
            max(len(src) * mismatch_cost, len(tar) * mismatch_cost)
        )