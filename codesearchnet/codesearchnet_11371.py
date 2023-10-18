def sim(self, src, tar, threshold=0.25, max_mismatches=2):
        """Return the MLIPNS similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        threshold : float
            A number [0, 1] indicating the maximum similarity score, below
            which the strings are considered 'similar' (0.25 by default)
        max_mismatches : int
            A number indicating the allowable number of mismatches to remove
            before declaring two strings not similar (2 by default)

        Returns
        -------
        float
            MLIPNS similarity

        Examples
        --------
        >>> sim_mlipns('cat', 'hat')
        1.0
        >>> sim_mlipns('Niall', 'Neil')
        0.0
        >>> sim_mlipns('aluminum', 'Catalan')
        0.0
        >>> sim_mlipns('ATCG', 'TAGC')
        0.0

        """
        if tar == src:
            return 1.0
        if not src or not tar:
            return 0.0

        mismatches = 0
        ham = Hamming().dist_abs(src, tar, diff_lens=True)
        max_length = max(len(src), len(tar))
        while src and tar and mismatches <= max_mismatches:
            if (
                max_length < 1
                or (1 - (max_length - ham) / max_length) <= threshold
            ):
                return 1.0
            else:
                mismatches += 1
                ham -= 1
                max_length -= 1

        if max_length < 1:
            return 1.0
        return 0.0