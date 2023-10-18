def dist(self, src, tar):
        """Return the NCD between two strings using zlib compression.

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
        >>> cmp = NCDzlib()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.45454545454545453
        >>> cmp.dist('aluminum', 'Catalan')
        0.5714285714285714
        >>> cmp.dist('ATCG', 'TAGC')
        0.4

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        self._compressor.compress(src)
        src_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(tar)
        tar_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(src + tar)
        concat_comp = self._compressor.flush(zlib.Z_FULL_FLUSH)
        self._compressor.compress(tar + src)
        concat_comp2 = self._compressor.flush(zlib.Z_FULL_FLUSH)

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))