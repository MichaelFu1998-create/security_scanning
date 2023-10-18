def dist_abs(
        self, src, tar, qval=2, pval=1, normalized=False, alphabet=None
    ):
        """Return the Minkowski distance (:math:`L^p`-norm) of two strings.

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
        normalized : bool
            Normalizes to [0, 1] if True
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        9.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0

        """
        q_src, q_tar = self._get_qgrams(src, tar, qval)
        diffs = ((q_src - q_tar) + (q_tar - q_src)).values()

        normalizer = 1
        if normalized:
            totals = (q_src + q_tar).values()
            if alphabet is not None:
                # noinspection PyTypeChecker
                normalizer = (
                    alphabet if isinstance(alphabet, Number) else len(alphabet)
                )
            elif pval == 0:
                normalizer = len(totals)
            else:
                normalizer = sum(_ ** pval for _ in totals) ** (1 / pval)

        if len(diffs) == 0:
            return 0.0
        if pval == float('inf'):
            # Chebyshev distance
            return max(diffs) / normalizer
        if pval == 0:
            # This is the l_0 "norm" as developed by David Donoho
            return len(diffs) / normalizer
        return sum(_ ** pval for _ in diffs) ** (1 / pval) / normalizer