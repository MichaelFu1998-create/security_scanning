def dist(self, src, tar, max_offset=5, max_distance=0):
        """Return the normalized "common" Sift4 distance between two terms.

        This is Sift4 distance, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        max_offset : int
            The number of characters to search for matching letters
        max_distance : int
            The distance at which to stop and exit

        Returns
        -------
        float
            The normalized Sift4 distance

        Examples
        --------
        >>> cmp = Sift4()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('Colin', 'Cuilen')
        0.5
        >>> cmp.dist('ATCG', 'TAGC')
        0.5

        """
        return self.dist_abs(src, tar, max_offset, max_distance) / (
            max(len(src), len(tar), 1)
        )