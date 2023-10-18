def dist_abs(self, src, tar, qval=2, alphabet=None):
        r"""Return the Chebyshev distance between two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version alphabet
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The Chebyshev distance

        Examples
        --------
        >>> cmp = Chebyshev()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        1.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.0
        >>> cmp.dist_abs('ATCG', 'TAGC', qval=1)
        0.0
        >>> cmp.dist_abs('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
        3.0

        """
        return super(self.__class__, self).dist_abs(
            src, tar, qval, float('inf'), False, alphabet
        )