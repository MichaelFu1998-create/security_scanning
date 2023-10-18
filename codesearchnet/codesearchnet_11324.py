def _synoname_word_approximation(
        self, src_ln, tar_ln, src_fn='', tar_fn='', features=None
    ):
        """Return the Synoname word approximation score for two names.

        Parameters
        ----------
        src_ln : str
            Last name of the source
        tar_ln : str
            Last name of the target
        src_fn : str
            First name of the source (optional)
        tar_fn : str
            First name of the target (optional)
        features : dict
            A dict containing special features calculated using
            :py:class:`fingerprint.SynonameToolcode` (optional)

        Returns
        -------
        float
            The word approximation score

        Examples
        --------
        >>> pe = Synoname()
        >>> pe._synoname_word_approximation('Smith Waterman', 'Waterman',
        ... 'Tom Joe Bob', 'Tom Joe')
        0.6

        """
        if features is None:
            features = {}
        if 'src_specials' not in features:
            features['src_specials'] = []
        if 'tar_specials' not in features:
            features['tar_specials'] = []

        src_len_specials = len(features['src_specials'])
        tar_len_specials = len(features['tar_specials'])

        # 1
        if ('gen_conflict' in features and features['gen_conflict']) or (
            'roman_conflict' in features and features['roman_conflict']
        ):
            return 0

        # 3 & 7
        full_tar1 = ' '.join((tar_ln, tar_fn)).replace('-', ' ').strip()
        for s_pos, s_type in features['tar_specials']:
            if s_type == 'a':
                full_tar1 = full_tar1[
                    : -(
                        1
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        )
                    )
                ]
            elif s_type == 'b':
                loc = (
                    full_tar1.find(
                        ' '
                        + self._stc._synoname_special_table[  # noqa: SF01
                            s_pos
                        ][1]
                        + ' '
                    )
                    + 1
                )
                full_tar1 = (
                    full_tar1[:loc]
                    + full_tar1[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )
            elif s_type == 'c':
                full_tar1 = full_tar1[
                    1
                    + len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]

        full_src1 = ' '.join((src_ln, src_fn)).replace('-', ' ').strip()
        for s_pos, s_type in features['src_specials']:
            if s_type == 'a':
                full_src1 = full_src1[
                    : -(
                        1
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        )
                    )
                ]
            elif s_type == 'b':
                loc = (
                    full_src1.find(
                        ' '
                        + self._stc._synoname_special_table[  # noqa: SF01
                            s_pos
                        ][1]
                        + ' '
                    )
                    + 1
                )
                full_src1 = (
                    full_src1[:loc]
                    + full_src1[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )
            elif s_type == 'c':
                full_src1 = full_src1[
                    1
                    + len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]

        full_tar2 = full_tar1
        for s_pos, s_type in features['tar_specials']:
            if s_type == 'd':
                full_tar2 = full_tar2[
                    len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]
            elif (
                s_type == 'X'
                and self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                in full_tar2
            ):
                loc = full_tar2.find(
                    ' '
                    + self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                )
                full_tar2 = (
                    full_tar2[:loc]
                    + full_tar2[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )

        full_src2 = full_src1
        for s_pos, s_type in features['src_specials']:
            if s_type == 'd':
                full_src2 = full_src2[
                    len(
                        self._stc._synoname_special_table[s_pos][  # noqa: SF01
                            1
                        ]
                    ) :
                ]
            elif (
                s_type == 'X'
                and self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                in full_src2
            ):
                loc = full_src2.find(
                    ' '
                    + self._stc._synoname_special_table[s_pos][1]  # noqa: SF01
                )
                full_src2 = (
                    full_src2[:loc]
                    + full_src2[
                        loc
                        + len(
                            self._stc._synoname_special_table[  # noqa: SF01
                                s_pos
                            ][1]
                        ) :
                    ]
                )

        full_tar1 = self._synoname_strip_punct(full_tar1)
        tar1_words = full_tar1.split()
        tar1_num_words = len(tar1_words)

        full_src1 = self._synoname_strip_punct(full_src1)
        src1_words = full_src1.split()
        src1_num_words = len(src1_words)

        full_tar2 = self._synoname_strip_punct(full_tar2)
        tar2_words = full_tar2.split()
        tar2_num_words = len(tar2_words)

        full_src2 = self._synoname_strip_punct(full_src2)
        src2_words = full_src2.split()
        src2_num_words = len(src2_words)

        # 2
        if (
            src1_num_words < 2
            and src_len_specials == 0
            and src2_num_words < 2
            and tar_len_specials == 0
        ):
            return 0

        # 4
        if (
            tar1_num_words == 1
            and src1_num_words == 1
            and tar1_words[0] == src1_words[0]
        ):
            return 1
        if tar1_num_words < 2 and tar_len_specials == 0:
            return 0

        # 5
        last_found = False
        for word in tar1_words:
            if src_ln.endswith(word) or word + ' ' in src_ln:
                last_found = True

        if not last_found:
            for word in src1_words:
                if tar_ln.endswith(word) or word + ' ' in tar_ln:
                    last_found = True

        # 6
        matches = 0
        if last_found:
            for i, s_word in enumerate(src1_words):
                for j, t_word in enumerate(tar1_words):
                    if s_word == t_word:
                        src1_words[i] = '@'
                        tar1_words[j] = '@'
                        matches += 1
        w_ratio = matches / max(tar1_num_words, src1_num_words)
        if matches > 1 or (
            matches == 1
            and src1_num_words == 1
            and tar1_num_words == 1
            and (tar_len_specials > 0 or src_len_specials > 0)
        ):
            return w_ratio

        # 8
        if (
            tar2_num_words == 1
            and src2_num_words == 1
            and tar2_words[0] == src2_words[0]
        ):
            return 1
        # I see no way that the following can be True if the equivalent in
        # #4 was False.
        if tar2_num_words < 2 and tar_len_specials == 0:  # pragma: no cover
            return 0

        # 9
        last_found = False
        for word in tar2_words:
            if src_ln.endswith(word) or word + ' ' in src_ln:
                last_found = True

        if not last_found:
            for word in src2_words:
                if tar_ln.endswith(word) or word + ' ' in tar_ln:
                    last_found = True

        if not last_found:
            return 0

        # 10
        matches = 0
        if last_found:
            for i, s_word in enumerate(src2_words):
                for j, t_word in enumerate(tar2_words):
                    if s_word == t_word:
                        src2_words[i] = '@'
                        tar2_words[j] = '@'
                        matches += 1
        w_ratio = matches / max(tar2_num_words, src2_num_words)
        if matches > 1 or (
            matches == 1
            and src2_num_words == 1
            and tar2_num_words == 1
            and (tar_len_specials > 0 or src_len_specials > 0)
        ):
            return w_ratio

        return 0