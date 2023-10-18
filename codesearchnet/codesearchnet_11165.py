def sim(self, src, tar, long_strings=False):
        """Return the strcmp95 similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        long_strings : bool
            Set to True to increase the probability of a match when the number
            of matched characters is large. This option allows for a little
            more tolerance when the strings are large. It is not an appropriate
            test when comparing fixed length fields such as phone and social
            security numbers.

        Returns
        -------
        float
            Strcmp95 similarity

        Examples
        --------
        >>> cmp = Strcmp95()
        >>> cmp.sim('cat', 'hat')
        0.7777777777777777
        >>> cmp.sim('Niall', 'Neil')
        0.8454999999999999
        >>> cmp.sim('aluminum', 'Catalan')
        0.6547619047619048
        >>> cmp.sim('ATCG', 'TAGC')
        0.8333333333333334

        """

        def _in_range(char):
            """Return True if char is in the range (0, 91).

            Parameters
            ----------
            char : str
                The character to check

            Returns
            -------
            bool
                True if char is in the range (0, 91)

            """
            return 91 > ord(char) > 0

        ying = src.strip().upper()
        yang = tar.strip().upper()

        if ying == yang:
            return 1.0
        # If either string is blank - return - added in Version 2
        if not ying or not yang:
            return 0.0

        adjwt = defaultdict(int)

        # Initialize the adjwt array on the first call to the function only.
        # The adjwt array is used to give partial credit for characters that
        # may be errors due to known phonetic or character recognition errors.
        # A typical example is to match the letter "O" with the number "0"
        for i in self._sp_mx:
            adjwt[(i[0], i[1])] = 3
            adjwt[(i[1], i[0])] = 3

        if len(ying) > len(yang):
            search_range = len(ying)
            minv = len(yang)
        else:
            search_range = len(yang)
            minv = len(ying)

        # Blank out the flags
        ying_flag = [0] * search_range
        yang_flag = [0] * search_range
        search_range = max(0, search_range // 2 - 1)

        # Looking only within the search range,
        # count and flag the matched pairs.
        num_com = 0
        yl1 = len(yang) - 1
        for i in range(len(ying)):
            low_lim = (i - search_range) if (i >= search_range) else 0
            hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
            for j in range(low_lim, hi_lim + 1):
                if (yang_flag[j] == 0) and (yang[j] == ying[i]):
                    yang_flag[j] = 1
                    ying_flag[i] = 1
                    num_com += 1
                    break

        # If no characters in common - return
        if num_com == 0:
            return 0.0

        # Count the number of transpositions
        k = n_trans = 0
        for i in range(len(ying)):
            if ying_flag[i] != 0:
                j = 0
                for j in range(k, len(yang)):  # pragma: no branch
                    if yang_flag[j] != 0:
                        k = j + 1
                        break
                if ying[i] != yang[j]:
                    n_trans += 1
        n_trans //= 2

        # Adjust for similarities in unmatched characters
        n_simi = 0
        if minv > num_com:
            for i in range(len(ying)):
                if ying_flag[i] == 0 and _in_range(ying[i]):
                    for j in range(len(yang)):
                        if yang_flag[j] == 0 and _in_range(yang[j]):
                            if (ying[i], yang[j]) in adjwt:
                                n_simi += adjwt[(ying[i], yang[j])]
                                yang_flag[j] = 2
                                break
        num_sim = n_simi / 10.0 + num_com

        # Main weight computation
        weight = (
            num_sim / len(ying)
            + num_sim / len(yang)
            + (num_com - n_trans) / num_com
        )
        weight /= 3.0

        # Continue to boost the weight if the strings are similar
        if weight > 0.7:

            # Adjust for having up to the first 4 characters in common
            j = 4 if (minv >= 4) else minv
            i = 0
            while (i < j) and (ying[i] == yang[i]) and (not ying[i].isdigit()):
                i += 1
            if i:
                weight += i * 0.1 * (1.0 - weight)

            # Optionally adjust for long strings.

            # After agreeing beginning chars, at least two more must agree and
            # the agreeing characters must be > .5 of remaining characters.
            if (
                long_strings
                and (minv > 4)
                and (num_com > i + 1)
                and (2 * num_com >= minv + i)
            ):
                if not ying[0].isdigit():
                    weight += (1.0 - weight) * (
                        (num_com - i - 1) / (len(ying) + len(yang) - i * 2 + 2)
                    )

        return weight