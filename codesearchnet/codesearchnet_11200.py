def dist_abs(self, src, tar, max_offset=5):
        """Return the "simplest" Sift4 distance between two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        max_offset : int
            The number of characters to search for matching letters

        Returns
        -------
        int
            The Sift4 distance according to the simplest formula

        Examples
        --------
        >>> cmp = Sift4Simplest()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2

        """
        if not src:
            return len(tar)

        if not tar:
            return len(src)

        src_len = len(src)
        tar_len = len(tar)

        src_cur = 0
        tar_cur = 0
        lcss = 0
        local_cs = 0

        while (src_cur < src_len) and (tar_cur < tar_len):
            if src[src_cur] == tar[tar_cur]:
                local_cs += 1
            else:
                lcss += local_cs
                local_cs = 0
                if src_cur != tar_cur:
                    src_cur = tar_cur = max(src_cur, tar_cur)
                for i in range(max_offset):
                    if not (
                        (src_cur + i < src_len) or (tar_cur + i < tar_len)
                    ):
                        break
                    if (src_cur + i < src_len) and (
                        src[src_cur + i] == tar[tar_cur]
                    ):
                        src_cur += i
                        local_cs += 1
                        break
                    if (tar_cur + i < tar_len) and (
                        src[src_cur] == tar[tar_cur + i]
                    ):
                        tar_cur += i
                        local_cs += 1
                        break

            src_cur += 1
            tar_cur += 1

        lcss += local_cs
        return round(max(src_len, tar_len) - lcss)