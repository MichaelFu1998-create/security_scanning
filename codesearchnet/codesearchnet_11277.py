def sim(self, src, tar, sim_func=sim_levenshtein, symmetric=False):
        """Return the Monge-Elkan similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        sim_func : function
            The internal similarity metric to employ
        symmetric : bool
            Return a symmetric similarity measure

        Returns
        -------
        float
            Monge-Elkan similarity

        Examples
        --------
        >>> cmp = MongeElkan()
        >>> cmp.sim('cat', 'hat')
        0.75
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.666666666667
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.388888888889
        >>> cmp.sim('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 1.0

        q_src = sorted(QGrams(src).elements())
        q_tar = sorted(QGrams(tar).elements())

        if not q_src or not q_tar:
            return 0.0

        sum_of_maxes = 0
        for q_s in q_src:
            max_sim = float('-inf')
            for q_t in q_tar:
                max_sim = max(max_sim, sim_func(q_s, q_t))
            sum_of_maxes += max_sim
        sim_em = sum_of_maxes / len(q_src)

        if symmetric:
            sim_em = (sim_em + self.sim(tar, src, sim_func, False)) / 2

        return sim_em