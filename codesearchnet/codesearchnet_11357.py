def dist_abs(self, src, tar, cost=(1, 1, 1, 1)):
        """Return the Damerau-Levenshtein distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 1))

        Returns
        -------
        int (may return a float if cost has float values)
            The Damerau-Levenshtein distance between src & tar

        Raises
        ------
        ValueError
            Unsupported cost assignment; the cost of two transpositions must
            not be less than the cost of an insert plus a delete.

        Examples
        --------
        >>> cmp = DamerauLevenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2

        """
        ins_cost, del_cost, sub_cost, trans_cost = cost

        if src == tar:
            return 0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        if 2 * trans_cost < ins_cost + del_cost:
            raise ValueError(
                'Unsupported cost assignment; the cost of two transpositions '
                + 'must not be less than the cost of an insert plus a delete.'
            )

        d_mat = np_zeros((len(src)) * (len(tar)), dtype=np_int).reshape(
            (len(src), len(tar))
        )

        if src[0] != tar[0]:
            d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

        src_index_by_character = {src[0]: 0}
        for i in range(1, len(src)):
            del_distance = d_mat[i - 1, 0] + del_cost
            ins_distance = (i + 1) * del_cost + ins_cost
            match_distance = i * del_cost + (
                0 if src[i] == tar[0] else sub_cost
            )
            d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

        for j in range(1, len(tar)):
            del_distance = (j + 1) * ins_cost + del_cost
            ins_distance = d_mat[0, j - 1] + ins_cost
            match_distance = j * ins_cost + (
                0 if src[0] == tar[j] else sub_cost
            )
            d_mat[0, j] = min(del_distance, ins_distance, match_distance)

        for i in range(1, len(src)):
            max_src_letter_match_index = 0 if src[i] == tar[0] else -1
            for j in range(1, len(tar)):
                candidate_swap_index = (
                    -1
                    if tar[j] not in src_index_by_character
                    else src_index_by_character[tar[j]]
                )
                j_swap = max_src_letter_match_index
                del_distance = d_mat[i - 1, j] + del_cost
                ins_distance = d_mat[i, j - 1] + ins_cost
                match_distance = d_mat[i - 1, j - 1]
                if src[i] != tar[j]:
                    match_distance += sub_cost
                else:
                    max_src_letter_match_index = j

                if candidate_swap_index != -1 and j_swap != -1:
                    i_swap = candidate_swap_index

                    if i_swap == 0 and j_swap == 0:
                        pre_swap_cost = 0
                    else:
                        pre_swap_cost = d_mat[
                            max(0, i_swap - 1), max(0, j_swap - 1)
                        ]
                    swap_distance = (
                        pre_swap_cost
                        + (i - i_swap - 1) * del_cost
                        + (j - j_swap - 1) * ins_cost
                        + trans_cost
                    )
                else:
                    swap_distance = maxsize

                d_mat[i, j] = min(
                    del_distance, ins_distance, match_distance, swap_distance
                )
            src_index_by_character[src[i]] = i

        return d_mat[len(src) - 1, len(tar) - 1]