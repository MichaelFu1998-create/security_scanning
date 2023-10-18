def dist(self, src, tar):
        """Return the normalized indel distance between two strings.

        This is equivalent to normalized Levenshtein distance, when only
        inserts and deletes are possible.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized indel distance

        Examples
        --------
        >>> cmp = Indel()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.333333333333
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.454545454545
        >>> cmp.dist('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / (len(src) + len(tar))