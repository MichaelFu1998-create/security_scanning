def dist_abs(self, src, tar):
        """Return the indel distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Indel distance

        Examples
        --------
        >>> cmp = Indel()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('Colin', 'Cuilen')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4

        """
        return self._lev.dist_abs(
            src, tar, mode='lev', cost=(1, 1, 9999, 9999)
        )