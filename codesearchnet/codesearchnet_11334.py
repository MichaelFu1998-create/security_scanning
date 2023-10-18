def dist(self, src, tar):
        """Return the NCD between two strings using bzip2 compression.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDbz2()
        >>> cmp.dist('cat', 'hat')
        0.06666666666666667
        >>> cmp.dist('Niall', 'Neil')
        0.03125
        >>> cmp.dist('aluminum', 'Catalan')
        0.17647058823529413
        >>> cmp.dist('ATCG', 'TAGC')
        0.03125

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        src_comp = bz2.compress(src, self._level)[10:]
        tar_comp = bz2.compress(tar, self._level)[10:]
        concat_comp = bz2.compress(src + tar, self._level)[10:]
        concat_comp2 = bz2.compress(tar + src, self._level)[10:]

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))