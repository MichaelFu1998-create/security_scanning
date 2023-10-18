def sim(self, src, tar):
        r"""Return the longest common subsequence similarity of two strings.

        Longest common subsequence similarity (:math:`sim_{LCSseq}`).

        This employs the LCSseq function to derive a similarity metric:
        :math:`sim_{LCSseq}(s,t) = \frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSseq similarity

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.sim('cat', 'hat')
        0.6666666666666666
        >>> sseq.sim('Niall', 'Neil')
        0.6
        >>> sseq.sim('aluminum', 'Catalan')
        0.375
        >>> sseq.sim('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return len(self.lcsseq(src, tar)) / max(len(src), len(tar))