def fingerprint(self, lname, fname='', qual='', normalize=0):
        """Build the Synoname toolcode.

        Parameters
        ----------
        lname : str
            Last name
        fname : str
            First name (can be blank)
        qual : str
            Qualifier
        normalize : int
            Normalization mode (0, 1, or 2)

        Returns
        -------
        tuple
            The transformed names and the synoname toolcode

        Examples
        --------
        >>> st = SynonameToolcode()
        >>> st.fingerprint('hat')
        ('hat', '', '0000000003$$h')
        >>> st.fingerprint('niall')
        ('niall', '', '0000000005$$n')
        >>> st.fingerprint('colin')
        ('colin', '', '0000000005$$c')
        >>> st.fingerprint('atcg')
        ('atcg', '', '0000000004$$a')
        >>> st.fingerprint('entreatment')
        ('entreatment', '', '0000000011$$e')

        >>> st.fingerprint('Ste.-Marie', 'Count John II', normalize=2)
        ('ste.-marie ii', 'count john', '0200491310$015b049a127c$smcji')
        >>> st.fingerprint('Michelangelo IV', '', 'Workshop of')
        ('michelangelo iv', '', '3000550015$055b$mi')

        """
        lname = lname.lower()
        fname = fname.lower()
        qual = qual.lower()

        # Start with the basic code
        toolcode = ['0', '0', '0', '000', '00', '00', '$', '', '$', '']

        full_name = ' '.join((lname, fname))

        if qual in self._qual_3:
            toolcode[0] = '3'
        elif qual in self._qual_2:
            toolcode[0] = '2'
        elif qual in self._qual_1:
            toolcode[0] = '1'

        # Fill field 1 (punctuation)
        if '.' in full_name:
            toolcode[1] = '2'
        else:
            for punct in ',-/:;"&\'()!{|}?$%*+<=>[\\]^_`~':
                if punct in full_name:
                    toolcode[1] = '1'
                    break

        elderyounger = ''  # save elder/younger for possible movement later
        for gen in self._gen_1:
            if gen in full_name:
                toolcode[2] = '1'
                elderyounger = gen
                break
        else:
            for gen in self._gen_2:
                if gen in full_name:
                    toolcode[2] = '2'
                    elderyounger = gen
                    break

        # do comma flip
        if normalize:
            comma = lname.find(',')
            if comma != -1:
                lname_end = lname[comma + 1 :]
                while lname_end[0] in {' ', ','}:
                    lname_end = lname_end[1:]
                fname = lname_end + ' ' + fname
                lname = lname[:comma].strip()

        # do elder/younger move
        if normalize == 2 and elderyounger:
            elderyounger_loc = fname.find(elderyounger)
            if elderyounger_loc != -1:
                lname = ' '.join((lname, elderyounger.strip()))
                fname = ' '.join(
                    (
                        fname[:elderyounger_loc].strip(),
                        fname[elderyounger_loc + len(elderyounger) :],
                    )
                ).strip()

        toolcode[4] = '{:02d}'.format(len(fname))
        toolcode[5] = '{:02d}'.format(len(lname))

        # strip punctuation
        for char in ',/:;"&()!{|}?$%*+<=>[\\]^_`~':
            full_name = full_name.replace(char, '')
        for pos, char in enumerate(full_name):
            if char == '-' and full_name[pos - 1 : pos + 2] != 'b-g':
                full_name = full_name[:pos] + ' ' + full_name[pos + 1 :]

        # Fill field 9 (search range)
        for letter in [_[0] for _ in full_name.split()]:
            if letter not in toolcode[9]:
                toolcode[9] += letter
            if len(toolcode[9]) == 15:
                break

        def roman_check(numeral, fname, lname):
            """Move Roman numerals from first name to last.

            Parameters
            ----------
            numeral : str
                Roman numeral
            fname : str
                First name
            lname : str
                Last name

            Returns
            -------
            tuple
                First and last names with Roman numeral moved

            """
            loc = fname.find(numeral)
            if fname and (
                loc != -1
                and (len(fname[loc:]) == len(numeral))
                or fname[loc + len(numeral)] in {' ', ','}
            ):
                lname = ' '.join((lname, numeral))
                fname = ' '.join(
                    (
                        fname[:loc].strip(),
                        fname[loc + len(numeral) :].lstrip(' ,'),
                    )
                )
            return fname.strip(), lname.strip()

        # Fill fields 7 (specials) and 3 (roman numerals)
        for num, special in enumerate(self._synoname_special_table):
            roman, match, extra, method = special
            if method & self._method_dict['end']:
                match_context = ' ' + match
                loc = full_name.find(match_context)
                if (len(full_name) > len(match_context)) and (
                    loc == len(full_name) - len(match_context)
                ):
                    if roman:
                        if not any(
                            abbr in fname for abbr in ('i.', 'v.', 'x.')
                        ):
                            full_name = full_name[:loc]
                            toolcode[7] += '{:03d}'.format(num) + 'a'
                            if toolcode[3] == '000':
                                toolcode[3] = '{:03d}'.format(num)
                            if normalize == 2:
                                fname, lname = roman_check(match, fname, lname)
                    else:
                        full_name = full_name[:loc]
                        toolcode[7] += '{:03d}'.format(num) + 'a'
            if method & self._method_dict['middle']:
                match_context = ' ' + match + ' '
                loc = 0
                while loc != -1:
                    loc = full_name.find(match_context, loc + 1)
                    if loc > 0:
                        if roman:
                            if not any(
                                abbr in fname for abbr in ('i.', 'v.', 'x.')
                            ):
                                full_name = (
                                    full_name[:loc]
                                    + full_name[loc + len(match) + 1 :]
                                )
                                toolcode[7] += '{:03d}'.format(num) + 'b'
                                if toolcode[3] == '000':
                                    toolcode[3] = '{:03d}'.format(num)
                                if normalize == 2:
                                    fname, lname = roman_check(
                                        match, fname, lname
                                    )
                        else:
                            full_name = (
                                full_name[:loc]
                                + full_name[loc + len(match) + 1 :]
                            )
                            toolcode[7] += '{:03d}'.format(num) + 'b'
            if method & self._method_dict['beginning']:
                match_context = match + ' '
                loc = full_name.find(match_context)
                if loc == 0:
                    full_name = full_name[len(match) + 1 :]
                    toolcode[7] += '{:03d}'.format(num) + 'c'
            if method & self._method_dict['beginning_no_space']:
                loc = full_name.find(match)
                if loc == 0:
                    toolcode[7] += '{:03d}'.format(num) + 'd'
                    if full_name[: len(match)] not in toolcode[9]:
                        toolcode[9] += full_name[: len(match)]

            if extra:
                loc = full_name.find(extra)
                if loc != -1:
                    toolcode[7] += '{:03d}'.format(num) + 'X'
                    # Since extras are unique, we only look for each of them
                    # once, and they include otherwise impossible characters
                    # for this field, it's not possible for the following line
                    # to have ever been false.
                    # if full_name[loc:loc+len(extra)] not in toolcode[9]:
                    toolcode[9] += full_name[loc : loc + len(match)]

        return lname, fname, ''.join(toolcode)