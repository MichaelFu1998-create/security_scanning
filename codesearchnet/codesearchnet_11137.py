def lcsseq(self, src, tar):
        """Return the longest common subsequence of two strings.

        Based on the dynamic programming algorithm from
        http://rosettacode.org/wiki/Longest_common_subsequence
        :cite:`rosettacode:2018b`. This is licensed GFDL 1.2.

        Modifications include:
            conversion to a numpy array in place of a list of lists

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common subsequence

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.lcsseq('cat', 'hat')
        'at'
        >>> sseq.lcsseq('Niall', 'Neil')
        'Nil'
        >>> sseq.lcsseq('aluminum', 'Catalan')
        'aln'
        >>> sseq.lcsseq('ATCG', 'TAGC')
        'AC'

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)

        # row 0 and column 0 are initialized to 0 already
        for i, src_char in enumerate(src):
            for j, tar_char in enumerate(tar):
                if src_char == tar_char:
                    lengths[i + 1, j + 1] = lengths[i, j] + 1
                else:
                    lengths[i + 1, j + 1] = max(
                        lengths[i + 1, j], lengths[i, j + 1]
                    )

        # read the substring out from the matrix
        result = ''
        i, j = len(src), len(tar)
        while i != 0 and j != 0:
            if lengths[i, j] == lengths[i - 1, j]:
                i -= 1
            elif lengths[i, j] == lengths[i, j - 1]:
                j -= 1
            else:
                result = src[i - 1] + result
                i -= 1
                j -= 1
        return result