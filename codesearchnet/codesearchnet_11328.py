def tanimoto_coeff(self, src, tar, qval=2):
        """Return the Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2} sim_{Tanimoto}(X, Y)`.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version

        Returns
        -------
        float
            Tanimoto distance

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf

        """
        coeff = self.sim(src, tar, qval)
        if coeff != 0:
            return log(coeff, 2)

        return float('-inf')