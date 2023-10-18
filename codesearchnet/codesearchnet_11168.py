def sim(self, src, tar):
        r"""Return the longest common substring similarity of two strings.

        Longest common substring similarity (:math:`sim_{LCSstr}`).

        This employs the LCS function to derive a similarity metric:
        :math:`sim_{LCSstr}(s,t) = \frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSstr similarity

        Examples
        --------
        >>> sim_lcsstr('cat', 'hat')
        0.6666666666666666
        >>> sim_lcsstr('Niall', 'Neil')
        0.2
        >>> sim_lcsstr('aluminum', 'Catalan')
        0.25
        >>> sim_lcsstr('ATCG', 'TAGC')
        0.25

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return len(self.lcsstr(src, tar)) / max(len(src), len(tar))