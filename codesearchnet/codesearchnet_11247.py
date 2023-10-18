def _get_qgrams(self, src, tar, qval=0, skip=0):
        """Return the Q-Grams in src & tar.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        skip : int
            The number of characters to skip (only works when src and tar are
            strings)

        Returns
        -------
        tuple of Counters
            Q-Grams

        Examples
        --------
        >>> pe = _TokenDistance()
        >>> pe._get_qgrams('AT', 'TT', qval=2)
        (QGrams({'$A': 1, 'AT': 1, 'T#': 1}),
         QGrams({'$T': 1, 'TT': 1, 'T#': 1}))

        """
        if isinstance(src, Counter) and isinstance(tar, Counter):
            return src, tar
        if qval > 0:
            return QGrams(src, qval, '$#', skip), QGrams(tar, qval, '$#', skip)
        return Counter(src.strip().split()), Counter(tar.strip().split())