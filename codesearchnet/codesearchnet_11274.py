def sim(self, src, tar, qval=2):
        r"""Return the cosine similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version

        Returns
        -------
        float
            Cosine similarity

        Examples
        --------
        >>> cmp = Cosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.11785113019775793
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        return q_intersection_mag / sqrt(q_src_mag * q_tar_mag)