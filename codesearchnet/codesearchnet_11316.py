def dist(self, src, tar, probs=None):
        """Return the NCD between two strings using arithmetic coding.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        probs : dict
            A dictionary trained with :py:meth:`Arithmetic.train`

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDarith()
        >>> cmp.dist('cat', 'hat')
        0.5454545454545454
        >>> cmp.dist('Niall', 'Neil')
        0.6875
        >>> cmp.dist('aluminum', 'Catalan')
        0.8275862068965517
        >>> cmp.dist('ATCG', 'TAGC')
        0.6923076923076923

        """
        if src == tar:
            return 0.0

        if probs is None:
            # lacking a reasonable dictionary, train on the strings themselves
            self._coder.train(src + tar)
        else:
            self._coder.set_probs(probs)

        src_comp = self._coder.encode(src)[1]
        tar_comp = self._coder.encode(tar)[1]
        concat_comp = self._coder.encode(src + tar)[1]
        concat_comp2 = self._coder.encode(tar + src)[1]

        return (
            min(concat_comp, concat_comp2) - min(src_comp, tar_comp)
        ) / max(src_comp, tar_comp)