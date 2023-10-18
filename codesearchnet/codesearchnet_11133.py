def sim(self, src, tar, min_ss_len=None, left_ext=None, right_ext=None):
        """Return the Baystat similarity.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        min_ss_len : int
            Minimum substring length to be considered
        left_ext :int
            Left-side extension length
        right_ext :int
            Right-side extension length

        Returns
        -------
        float
            The Baystat similarity

        Examples
        --------
        >>> cmp = Baystat()
        >>> round(cmp.sim('cat', 'hat'), 12)
        0.666666666667
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> round(cmp.sim('Colin', 'Cuilen'), 12)
        0.166666666667
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        max_len = max(len(src), len(tar))

        if not (min_ss_len and left_ext and right_ext):
            # These can be set via arguments to the function. Otherwise they
            # are set automatically based on values from the article.
            if max_len >= 7:
                min_ss_len = 2
                left_ext = 2
                right_ext = 2
            else:
                # The paper suggests that for short names, (exclusively) one or
                # the other of left_ext and right_ext can be 1, with good
                # results. I use 0 & 0 as the default in this case.
                min_ss_len = 1
                left_ext = 0
                right_ext = 0

        pos = 0
        match_len = 0

        while True:
            if pos + min_ss_len > len(src):
                return match_len / max_len

            hit_len = 0
            ix = 1

            substring = src[pos : pos + min_ss_len]
            search_begin = pos - left_ext

            if search_begin < 0:
                search_begin = 0
                left_ext_len = pos
            else:
                left_ext_len = left_ext

            if pos + min_ss_len + right_ext >= len(tar):
                right_ext_len = len(tar) - pos - min_ss_len
            else:
                right_ext_len = right_ext

            if (
                search_begin + left_ext_len + min_ss_len + right_ext_len
                > search_begin
            ):
                search_val = tar[
                    search_begin : (
                        search_begin
                        + left_ext_len
                        + min_ss_len
                        + right_ext_len
                    )
                ]
            else:
                search_val = ''

            flagged_tar = ''
            while substring in search_val and pos + ix <= len(src):
                hit_len = len(substring)
                flagged_tar = tar.replace(substring, '#' * hit_len)

                if pos + min_ss_len + ix <= len(src):
                    substring = src[pos : pos + min_ss_len + ix]

                if pos + min_ss_len + right_ext_len + 1 <= len(tar):
                    right_ext_len += 1

                # The following is unnecessary, I think
                # if (search_begin + left_ext_len + min_ss_len + right_ext_len
                #     <= len(tar)):
                search_val = tar[
                    search_begin : (
                        search_begin
                        + left_ext_len
                        + min_ss_len
                        + right_ext_len
                    )
                ]

                ix += 1

            if hit_len > 0:
                tar = flagged_tar

            match_len += hit_len
            pos += ix