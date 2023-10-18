def dist_abs(self, src, tar, gap_cost=1, sim_func=sim_ident):
        """Return the Smith-Waterman score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        gap_cost : float
            The cost of an alignment gap (1 by default)
        sim_func : function
            A function that returns the similarity of two characters (identity
            similarity by default)

        Returns
        -------
        float
            Smith-Waterman score

        Examples
        --------
        >>> cmp = SmithWaterman()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.0

        """
        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)

        for i in range(len(src) + 1):
            d_mat[i, 0] = 0
        for j in range(len(tar) + 1):
            d_mat[0, j] = 0
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                match = d_mat[i - 1, j - 1] + sim_func(src[i - 1], tar[j - 1])
                delete = d_mat[i - 1, j] - gap_cost
                insert = d_mat[i, j - 1] - gap_cost
                d_mat[i, j] = max(0, match, delete, insert)
        return d_mat[d_mat.shape[0] - 1, d_mat.shape[1] - 1]