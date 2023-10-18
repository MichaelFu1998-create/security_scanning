def encode(self, word, mode=1, lang='de'):
        """Return the phonet code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        mode : int
            The ponet variant to employ (1 or 2)
        lang : str
            ``de`` (default) for German, ``none`` for no language

        Returns
        -------
        str
            The phonet value

        Examples
        --------
        >>> pe = Phonet()
        >>> pe.encode('Christopher')
        'KRISTOFA'
        >>> pe.encode('Niall')
        'NIAL'
        >>> pe.encode('Smith')
        'SMIT'
        >>> pe.encode('Schmidt')
        'SHMIT'

        >>> pe.encode('Christopher', mode=2)
        'KRIZTUFA'
        >>> pe.encode('Niall', mode=2)
        'NIAL'
        >>> pe.encode('Smith', mode=2)
        'ZNIT'
        >>> pe.encode('Schmidt', mode=2)
        'ZNIT'

        >>> pe.encode('Christopher', lang='none')
        'CHRISTOPHER'
        >>> pe.encode('Niall', lang='none')
        'NIAL'
        >>> pe.encode('Smith', lang='none')
        'SMITH'
        >>> pe.encode('Schmidt', lang='none')
        'SCHMIDT'

        """
        phonet_hash = Counter()
        alpha_pos = Counter()

        phonet_hash_1 = Counter()
        phonet_hash_2 = Counter()

        def _initialize_phonet(lang):
            """Initialize phonet variables.

            Parameters
            ----------
            lang : str
                Language to use for rules

            """
            if lang == 'none':
                _phonet_rules = self._rules_no_lang
            else:
                _phonet_rules = self._rules_german

            phonet_hash[''] = -1

            # German and international umlauts
            for j in {
                'À',
                'Á',
                'Â',
                'Ã',
                'Ä',
                'Å',
                'Æ',
                'Ç',
                'È',
                'É',
                'Ê',
                'Ë',
                'Ì',
                'Í',
                'Î',
                'Ï',
                'Ð',
                'Ñ',
                'Ò',
                'Ó',
                'Ô',
                'Õ',
                'Ö',
                'Ø',
                'Ù',
                'Ú',
                'Û',
                'Ü',
                'Ý',
                'Þ',
                'ß',
                'Œ',
                'Š',
                'Ÿ',
            }:
                alpha_pos[j] = 1
                phonet_hash[j] = -1

            # "normal" letters ('A'-'Z')
            for i, j in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                alpha_pos[j] = i + 2
                phonet_hash[j] = -1

            for i in range(26):
                for j in range(28):
                    phonet_hash_1[i, j] = -1
                    phonet_hash_2[i, j] = -1

            # for each phonetc rule
            for i in range(len(_phonet_rules)):
                rule = _phonet_rules[i]

                if rule and i % 3 == 0:
                    # calculate first hash value
                    k = _phonet_rules[i][0]

                    if phonet_hash[k] < 0 and (
                        _phonet_rules[i + 1] or _phonet_rules[i + 2]
                    ):
                        phonet_hash[k] = i

                    # calculate second hash values
                    if k and alpha_pos[k] >= 2:
                        k = alpha_pos[k]

                        j = k - 2
                        rule = rule[1:]

                        if not rule:
                            rule = ' '
                        elif rule[0] == '(':
                            rule = rule[1:]
                        else:
                            rule = rule[0]

                        while rule and (rule[0] != ')'):
                            k = alpha_pos[rule[0]]

                            if k > 0:
                                # add hash value for this letter
                                if phonet_hash_1[j, k] < 0:
                                    phonet_hash_1[j, k] = i
                                    phonet_hash_2[j, k] = i

                                if phonet_hash_2[j, k] >= (i - 30):
                                    phonet_hash_2[j, k] = i
                                else:
                                    k = -1

                            if k <= 0:
                                # add hash value for all letters
                                if phonet_hash_1[j, 0] < 0:
                                    phonet_hash_1[j, 0] = i

                                phonet_hash_2[j, 0] = i

                            rule = rule[1:]

        def _phonet(term, mode, lang):
            """Return the phonet coded form of a term.

            Parameters
            ----------
            term : str
                Term to transform
            mode : int
                The ponet variant to employ (1 or 2)
            lang : str
                ``de`` (default) for German, ``none`` for no language

            Returns
            -------
            str
                The phonet value

            """
            if lang == 'none':
                _phonet_rules = self._rules_no_lang
            else:
                _phonet_rules = self._rules_german

            char0 = ''
            dest = term

            if not term:
                return ''

            term_length = len(term)

            # convert input string to upper-case
            src = term.translate(self._upper_trans)

            # check "src"
            i = 0
            j = 0
            zeta = 0

            while i < len(src):
                char = src[i]

                pos = alpha_pos[char]

                if pos >= 2:
                    xpos = pos - 2

                    if i + 1 == len(src):
                        pos = alpha_pos['']
                    else:
                        pos = alpha_pos[src[i + 1]]

                    start1 = phonet_hash_1[xpos, pos]
                    start2 = phonet_hash_1[xpos, 0]
                    end1 = phonet_hash_2[xpos, pos]
                    end2 = phonet_hash_2[xpos, 0]

                    # preserve rule priorities
                    if (start2 >= 0) and ((start1 < 0) or (start2 < start1)):
                        pos = start1
                        start1 = start2
                        start2 = pos
                        pos = end1
                        end1 = end2
                        end2 = pos

                    if (end1 >= start2) and (start2 >= 0):
                        if end2 > end1:
                            end1 = end2

                        start2 = -1
                        end2 = -1
                else:
                    pos = phonet_hash[char]
                    start1 = pos
                    end1 = 10000
                    start2 = -1
                    end2 = -1

                pos = start1
                zeta0 = 0

                if pos >= 0:
                    # check rules for this char
                    while (_phonet_rules[pos] is None) or (
                        _phonet_rules[pos][0] == char
                    ):
                        if pos > end1:
                            if start2 > 0:
                                pos = start2
                                start1 = start2
                                start2 = -1
                                end1 = end2
                                end2 = -1
                                continue

                            break

                        if (_phonet_rules[pos] is None) or (
                            _phonet_rules[pos + mode] is None
                        ):
                            # no conversion rule available
                            pos += 3
                            continue

                        # check whole string
                        matches = 1  # number of matching letters
                        priority = 5  # default priority
                        rule = _phonet_rules[pos]
                        rule = rule[1:]

                        while (
                            rule
                            and (len(src) > (i + matches))
                            and (src[i + matches] == rule[0])
                            and not rule[0].isdigit()
                            and (rule not in '(-<^$')
                        ):
                            matches += 1
                            rule = rule[1:]

                        if rule and (rule[0] == '('):
                            # check an array of letters
                            if (
                                (len(src) > (i + matches))
                                and src[i + matches].isalpha()
                                and (src[i + matches] in rule[1:])
                            ):
                                matches += 1

                                while rule and rule[0] != ')':
                                    rule = rule[1:]

                                # if rule[0] == ')':
                                rule = rule[1:]

                        if rule:
                            priority0 = ord(rule[0])
                        else:
                            priority0 = 0

                        matches0 = matches

                        while rule and rule[0] == '-' and matches > 1:
                            matches -= 1
                            rule = rule[1:]

                        if rule and rule[0] == '<':
                            rule = rule[1:]

                        if rule and rule[0].isdigit():
                            # read priority
                            priority = int(rule[0])
                            rule = rule[1:]

                        if rule and rule[0:2] == '^^':
                            rule = rule[1:]

                        if (
                            not rule
                            or (
                                (rule[0] == '^')
                                and ((i == 0) or not src[i - 1].isalpha())
                                and (
                                    (rule[1:2] != '$')
                                    or (
                                        not (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ].isalpha()
                                        )
                                        and (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ]
                                            != '.'
                                        )
                                    )
                                )
                            )
                            or (
                                (rule[0] == '$')
                                and (i > 0)
                                and src[i - 1].isalpha()
                                and (
                                    (
                                        not src[
                                            i + matches0 : i + matches0 + 1
                                        ].isalpha()
                                    )
                                    and (
                                        src[i + matches0 : i + matches0 + 1]
                                        != '.'
                                    )
                                )
                            )
                        ):
                            # look for continuation, if:
                            # matches > 1 und NO '-' in first string */
                            pos0 = -1

                            start3 = 0
                            start4 = 0
                            end3 = 0
                            end4 = 0

                            if (
                                (matches > 1)
                                and src[i + matches : i + matches + 1]
                                and (priority0 != ord('-'))
                            ):
                                char0 = src[i + matches - 1]
                                pos0 = alpha_pos[char0]

                                if pos0 >= 2 and src[i + matches]:
                                    xpos = pos0 - 2
                                    pos0 = alpha_pos[src[i + matches]]
                                    start3 = phonet_hash_1[xpos, pos0]
                                    start4 = phonet_hash_1[xpos, 0]
                                    end3 = phonet_hash_2[xpos, pos0]
                                    end4 = phonet_hash_2[xpos, 0]

                                    # preserve rule priorities
                                    if (start4 >= 0) and (
                                        (start3 < 0) or (start4 < start3)
                                    ):
                                        pos0 = start3
                                        start3 = start4
                                        start4 = pos0
                                        pos0 = end3
                                        end3 = end4
                                        end4 = pos0

                                    if (end3 >= start4) and (start4 >= 0):
                                        if end4 > end3:
                                            end3 = end4

                                        start4 = -1
                                        end4 = -1
                                else:
                                    pos0 = phonet_hash[char0]
                                    start3 = pos0
                                    end3 = 10000
                                    start4 = -1
                                    end4 = -1

                                pos0 = start3

                            # check continuation rules for src[i+matches]
                            if pos0 >= 0:
                                while (_phonet_rules[pos0] is None) or (
                                    _phonet_rules[pos0][0] == char0
                                ):
                                    if pos0 > end3:
                                        if start4 > 0:
                                            pos0 = start4
                                            start3 = start4
                                            start4 = -1
                                            end3 = end4
                                            end4 = -1
                                            continue

                                        priority0 = -1

                                        # important
                                        break

                                    if (_phonet_rules[pos0] is None) or (
                                        _phonet_rules[pos0 + mode] is None
                                    ):
                                        # no conversion rule available
                                        pos0 += 3
                                        continue

                                    # check whole string
                                    matches0 = matches
                                    priority0 = 5
                                    rule = _phonet_rules[pos0]
                                    rule = rule[1:]

                                    while (
                                        rule
                                        and (
                                            src[
                                                i + matches0 : i + matches0 + 1
                                            ]
                                            == rule[0]
                                        )
                                        and (
                                            not rule[0].isdigit()
                                            or (rule in '(-<^$')
                                        )
                                    ):
                                        matches0 += 1
                                        rule = rule[1:]

                                    if rule and rule[0] == '(':
                                        # check an array of letters
                                        if src[
                                            i + matches0 : i + matches0 + 1
                                        ].isalpha() and (
                                            src[i + matches0] in rule[1:]
                                        ):
                                            matches0 += 1

                                            while rule and rule[0] != ')':
                                                rule = rule[1:]

                                            # if rule[0] == ')':
                                            rule = rule[1:]

                                    while rule and rule[0] == '-':
                                        # "matches0" is NOT decremented
                                        # because of
                                        #    "if (matches0 == matches)"
                                        rule = rule[1:]

                                    if rule and rule[0] == '<':
                                        rule = rule[1:]

                                    if rule and rule[0].isdigit():
                                        priority0 = int(rule[0])
                                        rule = rule[1:]

                                    if (
                                        not rule
                                        or
                                        # rule == '^' is not possible here
                                        (
                                            (rule[0] == '$')
                                            and not src[
                                                i + matches0 : i + matches0 + 1
                                            ].isalpha()
                                            and (
                                                src[
                                                    i
                                                    + matches0 : i
                                                    + matches0
                                                    + 1
                                                ]
                                                != '.'
                                            )
                                        )
                                    ):
                                        if matches0 == matches:
                                            # this is only a partial string
                                            pos0 += 3
                                            continue

                                        if priority0 < priority:
                                            # priority is too low
                                            pos0 += 3
                                            continue

                                        # continuation rule found
                                        break

                                    pos0 += 3

                                # end of "while"
                                if (priority0 >= priority) and (
                                    (_phonet_rules[pos0] is not None)
                                    and (_phonet_rules[pos0][0] == char0)
                                ):

                                    pos += 3
                                    continue

                            # replace string
                            if _phonet_rules[pos] and (
                                '<' in _phonet_rules[pos][1:]
                            ):
                                priority0 = 1
                            else:
                                priority0 = 0

                            rule = _phonet_rules[pos + mode]

                            if (priority0 == 1) and (zeta == 0):
                                # rule with '<' is applied
                                if (
                                    (j > 0)
                                    and rule
                                    and (
                                        (dest[j - 1] == char)
                                        or (dest[j - 1] == rule[0])
                                    )
                                ):
                                    j -= 1

                                zeta0 = 1
                                zeta += 1
                                matches0 = 0

                                while rule and src[i + matches0]:
                                    src = (
                                        src[0 : i + matches0]
                                        + rule[0]
                                        + src[i + matches0 + 1 :]
                                    )
                                    matches0 += 1
                                    rule = rule[1:]

                                if matches0 < matches:
                                    src = (
                                        src[0 : i + matches0]
                                        + src[i + matches :]
                                    )

                                char = src[i]
                            else:
                                i = i + matches - 1
                                zeta = 0

                                while len(rule) > 1:
                                    if (j == 0) or (dest[j - 1] != rule[0]):
                                        dest = (
                                            dest[0:j]
                                            + rule[0]
                                            + dest[min(len(dest), j + 1) :]
                                        )
                                        j += 1

                                    rule = rule[1:]

                                # new "current char"
                                if not rule:
                                    rule = ''
                                    char = ''
                                else:
                                    char = rule[0]

                                if (
                                    _phonet_rules[pos]
                                    and '^^' in _phonet_rules[pos][1:]
                                ):
                                    if char:
                                        dest = (
                                            dest[0:j]
                                            + char
                                            + dest[min(len(dest), j + 1) :]
                                        )
                                        j += 1

                                    src = src[i + 1 :]
                                    i = 0
                                    zeta0 = 1

                            break

                        pos += 3

                        if pos > end1 and start2 > 0:
                            pos = start2
                            start1 = start2
                            end1 = end2
                            start2 = -1
                            end2 = -1

                if zeta0 == 0:
                    if char and ((j == 0) or (dest[j - 1] != char)):
                        # delete multiple letters only
                        dest = (
                            dest[0:j] + char + dest[min(j + 1, term_length) :]
                        )
                        j += 1

                    i += 1
                    zeta = 0

            dest = dest[0:j]

            return dest

        _initialize_phonet(lang)

        word = unicode_normalize('NFKC', text_type(word))
        return _phonet(word, mode, lang)