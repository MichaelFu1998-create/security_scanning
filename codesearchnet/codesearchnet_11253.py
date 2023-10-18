def dist(self, src, tar):
        """Return the NCD between two strings using LZMA compression.

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

        Raises
        ------
        ValueError
            Install the PylibLZMA module in order to use LZMA

        Examples
        --------
        >>> cmp = NCDlzma()
        >>> cmp.dist('cat', 'hat')
        0.08695652173913043
        >>> cmp.dist('Niall', 'Neil')
        0.16
        >>> cmp.dist('aluminum', 'Catalan')
        0.16
        >>> cmp.dist('ATCG', 'TAGC')
        0.08695652173913043

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        if lzma is not None:
            src_comp = lzma.compress(src)[14:]
            tar_comp = lzma.compress(tar)[14:]
            concat_comp = lzma.compress(src + tar)[14:]
            concat_comp2 = lzma.compress(tar + src)[14:]
        else:  # pragma: no cover
            raise ValueError(
                'Install the PylibLZMA module in order to use LZMA'
            )

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))