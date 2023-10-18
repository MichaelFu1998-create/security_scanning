def dist_abs(self, src, tar, cost=(0, 1, 2), local=False):
        """Return the Editex distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        cost : tuple
            A 3-tuple representing the cost of the four possible edits: match,
            same-group, and mismatch respectively (by default: (0, 1, 2))
        local : bool
            If True, the local variant of Editex is used

        Returns
        -------
        int
            Editex distance

        Examples
        --------
        >>> cmp = Editex()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        12
        >>> cmp.dist_abs('ATCG', 'TAGC')
        6

        """
        match_cost, group_cost, mismatch_cost = cost

        def r_cost(ch1, ch2):
            """Return r(a,b) according to Zobel & Dart's definition.

            Parameters
            ----------
            ch1 : str
                The first character to compare
            ch2 : str
                The second character to compare

            Returns
            -------
            int
                r(a,b) according to Zobel & Dart's definition

            """
            if ch1 == ch2:
                return match_cost
            if ch1 in self._all_letters and ch2 in self._all_letters:
                for group in self._letter_groups:
                    if ch1 in group and ch2 in group:
                        return group_cost
            return mismatch_cost

        def d_cost(ch1, ch2):
            """Return d(a,b) according to Zobel & Dart's definition.

            Parameters
            ----------
            ch1 : str
                The first character to compare
            ch2 : str
                The second character to compare

            Returns
            -------
            int
                d(a,b) according to Zobel & Dart's definition

            """
            if ch1 != ch2 and (ch1 == 'H' or ch1 == 'W'):
                return group_cost
            return r_cost(ch1, ch2)

        # convert both src & tar to NFKD normalized unicode
        src = unicode_normalize('NFKD', text_type(src.upper()))
        tar = unicode_normalize('NFKD', text_type(tar.upper()))
        # convert ß to SS (for Python2)
        src = src.replace('ß', 'SS')
        tar = tar.replace('ß', 'SS')

        if src == tar:
            return 0.0
        if not src:
            return len(tar) * mismatch_cost
        if not tar:
            return len(src) * mismatch_cost

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        lens = len(src)
        lent = len(tar)
        src = ' ' + src
        tar = ' ' + tar

        if not local:
            for i in range(1, lens + 1):
                d_mat[i, 0] = d_mat[i - 1, 0] + d_cost(src[i - 1], src[i])
        for j in range(1, lent + 1):
            d_mat[0, j] = d_mat[0, j - 1] + d_cost(tar[j - 1], tar[j])

        for i in range(1, lens + 1):
            for j in range(1, lent + 1):
                d_mat[i, j] = min(
                    d_mat[i - 1, j] + d_cost(src[i - 1], src[i]),
                    d_mat[i, j - 1] + d_cost(tar[j - 1], tar[j]),
                    d_mat[i - 1, j - 1] + r_cost(src[i], tar[j]),
                )

        return d_mat[lens, lent]