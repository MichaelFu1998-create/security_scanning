def sim(
        self,
        src,
        tar,
        qval=1,
        mode='winkler',
        long_strings=False,
        boost_threshold=0.7,
        scaling_factor=0.1,
    ):
        """Return the Jaro or Jaro-Winkler similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        qval : int
            The length of each q-gram (defaults to 1: character-wise matching)
        mode : str
            Indicates which variant of this distance metric to compute:

                - ``winkler`` -- computes the Jaro-Winkler distance (default)
                  which increases the score for matches near the start of the
                  word
                - ``jaro`` -- computes the Jaro distance

        long_strings : bool
            Set to True to "Increase the probability of a match when the number
            of matched characters is large. This option allows for a little
            more tolerance when the strings are large. It is not an appropriate
            test when comparing fixed length fields such as phone and social
            security numbers." (Used in 'winkler' mode only.)
        boost_threshold : float
            A value between 0 and 1, below which the Winkler boost is not
            applied (defaults to 0.7). (Used in 'winkler' mode only.)
        scaling_factor : float
            A value between 0 and 0.25, indicating by how much to boost scores
            for matching prefixes (defaults to 0.1). (Used in 'winkler' mode
            only.)

        Returns
        -------
        float
            Jaro or Jaro-Winkler similarity

        Raises
        ------
        ValueError
            Unsupported boost_threshold assignment; boost_threshold must be
            between 0 and 1.
        ValueError
            Unsupported scaling_factor assignment; scaling_factor must be
            between 0 and 0.25.'

        Examples
        --------
        >>> round(sim_jaro_winkler('cat', 'hat'), 12)
        0.777777777778
        >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
        0.805
        >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
        0.60119047619
        >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
        0.833333333333

        >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
        0.777777777778
        >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
        0.783333333333
        >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
        0.60119047619
        >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
        0.833333333333

        """
        if mode == 'winkler':
            if boost_threshold > 1 or boost_threshold < 0:
                raise ValueError(
                    'Unsupported boost_threshold assignment; '
                    + 'boost_threshold must be between 0 and 1.'
                )
            if scaling_factor > 0.25 or scaling_factor < 0:
                raise ValueError(
                    'Unsupported scaling_factor assignment; '
                    + 'scaling_factor must be between 0 and 0.25.'
                )

        if src == tar:
            return 1.0

        src = QGrams(src.strip(), qval)._ordered_list
        tar = QGrams(tar.strip(), qval)._ordered_list

        lens = len(src)
        lent = len(tar)

        # If either string is blank - return - added in Version 2
        if lens == 0 or lent == 0:
            return 0.0

        if lens > lent:
            search_range = lens
            minv = lent
        else:
            search_range = lent
            minv = lens

        # Zero out the flags
        src_flag = [0] * search_range
        tar_flag = [0] * search_range
        search_range = max(0, search_range // 2 - 1)

        # Looking only within the search range,
        # count and flag the matched pairs.
        num_com = 0
        yl1 = lent - 1
        for i in range(lens):
            low_lim = (i - search_range) if (i >= search_range) else 0
            hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
            for j in range(low_lim, hi_lim + 1):
                if (tar_flag[j] == 0) and (tar[j] == src[i]):
                    tar_flag[j] = 1
                    src_flag[i] = 1
                    num_com += 1
                    break

        # If no characters in common - return
        if num_com == 0:
            return 0.0

        # Count the number of transpositions
        k = n_trans = 0
        for i in range(lens):
            if src_flag[i] != 0:
                j = 0
                for j in range(k, lent):  # pragma: no branch
                    if tar_flag[j] != 0:
                        k = j + 1
                        break
                if src[i] != tar[j]:
                    n_trans += 1
        n_trans //= 2

        # Main weight computation for Jaro distance
        weight = (
            num_com / lens + num_com / lent + (num_com - n_trans) / num_com
        )
        weight /= 3.0

        # Continue to boost the weight if the strings are similar
        # This is the Winkler portion of Jaro-Winkler distance
        if mode == 'winkler' and weight > boost_threshold:

            # Adjust for having up to the first 4 characters in common
            j = 4 if (minv >= 4) else minv
            i = 0
            while (i < j) and (src[i] == tar[i]):
                i += 1
            weight += i * scaling_factor * (1.0 - weight)

            # Optionally adjust for long strings.

            # After agreeing beginning chars, at least two more must agree and
            # the agreeing characters must be > .5 of remaining characters.
            if (
                long_strings
                and (minv > 4)
                and (num_com > i + 1)
                and (2 * num_com >= minv + i)
            ):
                weight += (1.0 - weight) * (
                    (num_com - i - 1) / (lens + lent - i * 2 + 2)
                )

        return weight