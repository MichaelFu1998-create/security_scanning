def dist(self, src, tar, weights='exponential', max_length=8):
        """Return normalized distance between the Eudex hashes of two terms.

        This is Eudex distance normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        weights : str, iterable, or generator function
            The weights or weights generator function
        max_length : int
            The number of characters to encode as a eudex hash

        Returns
        -------
        int
            The normalized Eudex Hamming distance

        Examples
        --------
        >>> cmp = Eudex()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.062745098039
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.000980392157
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.004901960784
        >>> round(cmp.dist('ATCG', 'TAGC'), 12)
        0.197549019608

        """
        return self.dist_abs(src, tar, weights, max_length, True)