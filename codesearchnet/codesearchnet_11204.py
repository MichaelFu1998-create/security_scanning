def dist_abs(
        self,
        src,
        tar,
        metric='euclidean',
        cost=(1, 1, 0.5, 0.5),
        layout='QWERTY',
    ):
        """Return the typo distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        metric : str
            Supported values include: ``euclidean``, ``manhattan``,
            ``log-euclidean``, and ``log-manhattan``
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and shift, respectively (by
            default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
            significantly less than the cost of an insertion & deletion unless
            a log metric is used.
        layout : str
            Name of the keyboard layout to use (Currently supported:
            ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

        Returns
        -------
        float
            Typo distance

        Raises
        ------
        ValueError
            char not found in any keyboard layouts

        Examples
        --------
        >>> cmp = Typo()
        >>> cmp.dist_abs('cat', 'hat')
        1.5811388
        >>> cmp.dist_abs('Niall', 'Neil')
        2.8251407
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.4142137
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.5

        >>> cmp.dist_abs('cat', 'hat', metric='manhattan')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil', metric='manhattan')
        3.0
        >>> cmp.dist_abs('Colin', 'Cuilen', metric='manhattan')
        3.5
        >>> cmp.dist_abs('ATCG', 'TAGC', metric='manhattan')
        2.5

        >>> cmp.dist_abs('cat', 'hat', metric='log-manhattan')
        0.804719
        >>> cmp.dist_abs('Niall', 'Neil', metric='log-manhattan')
        2.2424533
        >>> cmp.dist_abs('Colin', 'Cuilen', metric='log-manhattan')
        2.2424533
        >>> cmp.dist_abs('ATCG', 'TAGC', metric='log-manhattan')
        2.3465736

        """
        ins_cost, del_cost, sub_cost, shift_cost = cost

        if src == tar:
            return 0.0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        keyboard = self._keyboard[layout]
        lowercase = {item for sublist in keyboard[0] for item in sublist}
        uppercase = {item for sublist in keyboard[1] for item in sublist}

        def _kb_array_for_char(char):
            """Return the keyboard layout that contains ch.

            Parameters
            ----------
            char : str
                The character to lookup

            Returns
            -------
            tuple
                A keyboard

            Raises
            ------
            ValueError
                char not found in any keyboard layouts

            """
            if char in lowercase:
                return keyboard[0]
            elif char in uppercase:
                return keyboard[1]
            raise ValueError(char + ' not found in any keyboard layouts')

        def _substitution_cost(char1, char2):
            cost = sub_cost
            cost *= metric_dict[metric](char1, char2) + shift_cost * (
                _kb_array_for_char(char1) != _kb_array_for_char(char2)
            )
            return cost

        def _get_char_coord(char, kb_array):
            """Return the row & column of char in the keyboard.

            Parameters
            ----------
            char : str
                The character to search for
            kb_array : tuple of tuples
                The array of key positions

            Returns
            -------
            tuple
                The row & column of the key

            """
            for row in kb_array:  # pragma: no branch
                if char in row:
                    return kb_array.index(row), row.index(char)

        def _euclidean_keyboard_distance(char1, char2):
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5

        def _manhattan_keyboard_distance(char1, char2):
            row1, col1 = _get_char_coord(char1, _kb_array_for_char(char1))
            row2, col2 = _get_char_coord(char2, _kb_array_for_char(char2))
            return abs(row1 - row2) + abs(col1 - col2)

        def _log_euclidean_keyboard_distance(char1, char2):
            return log(1 + _euclidean_keyboard_distance(char1, char2))

        def _log_manhattan_keyboard_distance(char1, char2):
            return log(1 + _manhattan_keyboard_distance(char1, char2))

        metric_dict = {
            'euclidean': _euclidean_keyboard_distance,
            'manhattan': _manhattan_keyboard_distance,
            'log-euclidean': _log_euclidean_keyboard_distance,
            'log-manhattan': _log_manhattan_keyboard_distance,
        }

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
        for i in range(len(src) + 1):
            d_mat[i, 0] = i * del_cost
        for j in range(len(tar) + 1):
            d_mat[0, j] = j * ins_cost

        for i in range(len(src)):
            for j in range(len(tar)):
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + ins_cost,  # ins
                    d_mat[i, j + 1] + del_cost,  # del
                    d_mat[i, j]
                    + (
                        _substitution_cost(src[i], tar[j])
                        if src[i] != tar[j]
                        else 0
                    ),  # sub/==
                )

        return d_mat[len(src), len(tar)]