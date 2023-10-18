def dist(self, src, tar):
        """Return the normalized bag distance between two strings.

        Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.0

        """
        if tar == src:
            return 0.0
        if not src or not tar:
            return 1.0

        max_length = max(len(src), len(tar))

        return self.dist_abs(src, tar) / max_length