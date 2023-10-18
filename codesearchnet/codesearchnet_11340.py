def dist_abs(self, src, tar):
        """Return the MRA comparison rating of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            MRA comparison rating

        Examples
        --------
        >>> cmp = MRA()
        >>> cmp.dist_abs('cat', 'hat')
        5
        >>> cmp.dist_abs('Niall', 'Neil')
        6
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        5

        """
        if src == tar:
            return 6
        if src == '' or tar == '':
            return 0
        src = list(mra(src))
        tar = list(mra(tar))

        if abs(len(src) - len(tar)) > 2:
            return 0

        length_sum = len(src) + len(tar)
        if length_sum < 5:
            min_rating = 5
        elif length_sum < 8:
            min_rating = 4
        elif length_sum < 12:
            min_rating = 3
        else:
            min_rating = 2

        for _ in range(2):
            new_src = []
            new_tar = []
            minlen = min(len(src), len(tar))
            for i in range(minlen):
                if src[i] != tar[i]:
                    new_src.append(src[i])
                    new_tar.append(tar[i])
            src = new_src + src[minlen:]
            tar = new_tar + tar[minlen:]
            src.reverse()
            tar.reverse()

        similarity = 6 - max(len(src), len(tar))

        if similarity >= min_rating:
            return similarity
        return 0