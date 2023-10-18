def dist(self, src, tar, qval=2, pval=1, alphabet=None):
        """Return normalized Minkowski distance of two strings.

        The normalized Minkowski distance :cite:`Minkowski:1910` is a distance
        metric in :math:`L^p`-space, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        pval : int or float
            The :math:`p`-value of the :math:`L^p`-space
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The normalized Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.636363636364
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.692307692308
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        """
        return self.dist_abs(src, tar, qval, pval, True, alphabet)