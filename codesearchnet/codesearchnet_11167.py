def lcsstr(self, src, tar):
        """Return the longest common substring of two strings.

        Longest common substring (LCSstr).

        Based on the code from
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
        :cite:`Wikibooks:2018`.
        This is licensed Creative Commons: Attribution-ShareAlike 3.0.

        Modifications include:

            - conversion to a numpy array in place of a list of lists
            - conversion to Python 2/3-safe range from xrange via six

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common substring

        Examples
        --------
        >>> sstr = LCSstr()
        >>> sstr.lcsstr('cat', 'hat')
        'at'
        >>> sstr.lcsstr('Niall', 'Neil')
        'N'
        >>> sstr.lcsstr('aluminum', 'Catalan')
        'al'
        >>> sstr.lcsstr('ATCG', 'TAGC')
        'A'

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        longest, i_longest = 0, 0
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                if src[i - 1] == tar[j - 1]:
                    lengths[i, j] = lengths[i - 1, j - 1] + 1
                    if lengths[i, j] > longest:
                        longest = lengths[i, j]
                        i_longest = i
                else:
                    lengths[i, j] = 0
        return src[i_longest - longest : i_longest]