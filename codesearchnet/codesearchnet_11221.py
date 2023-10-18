def encode(self, lname, max_length=4, german=False):
        """Calculate the PSHP Soundex/Viewex Coding of a last name.

        Parameters
        ----------
        lname : str
            The last name to encode
        max_length : int
            The length of the code returned (defaults to 4)
        german : bool
            Set to True if the name is German (different rules apply)

        Returns
        -------
        str
            The PSHP Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexLast()
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Waters')
        'W350'
        >>> pe.encode('James')
        'J500'
        >>> pe.encode('Schmidt')
        'S530'
        >>> pe.encode('Ashcroft')
        'A225'

        """
        lname = unicode_normalize('NFKD', text_type(lname.upper()))
        lname = lname.replace('ß', 'SS')
        lname = ''.join(c for c in lname if c in self._uc_set)

        # A. Prefix treatment
        if lname[:3] == 'VON' or lname[:3] == 'VAN':
            lname = lname[3:].strip()

        # The rule implemented below says "MC, MAC become 1". I believe it
        # meant to say they become M except in German data (where superscripted
        # 1 indicates "except in German data"). It doesn't make sense for them
        # to become 1 (BPFV -> 1) or to apply outside German. Unfortunately,
        # both articles have this error(?).
        if not german:
            if lname[:3] == 'MAC':
                lname = 'M' + lname[3:]
            elif lname[:2] == 'MC':
                lname = 'M' + lname[2:]

        # The non-German-only rule to strip ' is unnecessary due to filtering

        if lname[:1] in {'E', 'I', 'O', 'U'}:
            lname = 'A' + lname[1:]
        elif lname[:2] in {'GE', 'GI', 'GY'}:
            lname = 'J' + lname[1:]
        elif lname[:2] in {'CE', 'CI', 'CY'}:
            lname = 'S' + lname[1:]
        elif lname[:3] == 'CHR':
            lname = 'K' + lname[1:]
        elif lname[:1] == 'C' and lname[:2] != 'CH':
            lname = 'K' + lname[1:]

        if lname[:2] == 'KN':
            lname = 'N' + lname[1:]
        elif lname[:2] == 'PH':
            lname = 'F' + lname[1:]
        elif lname[:3] in {'WIE', 'WEI'}:
            lname = 'V' + lname[1:]

        if german and lname[:1] in {'W', 'M', 'Y', 'Z'}:
            lname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[lname[0]] + lname[
                1:
            ]

        code = lname[:1]

        # B. Postfix treatment
        if german:  # moved from end of postfix treatment due to blocking
            if lname[-3:] == 'TES':
                lname = lname[:-3]
            elif lname[-2:] == 'TS':
                lname = lname[:-2]
            if lname[-3:] == 'TZE':
                lname = lname[:-3]
            elif lname[-2:] == 'ZE':
                lname = lname[:-2]
            if lname[-1:] == 'Z':
                lname = lname[:-1]
            elif lname[-2:] == 'TE':
                lname = lname[:-2]

        if lname[-1:] == 'R':
            lname = lname[:-1] + 'N'
        elif lname[-2:] in {'SE', 'CE'}:
            lname = lname[:-2]
        if lname[-2:] == 'SS':
            lname = lname[:-2]
        elif lname[-1:] == 'S':
            lname = lname[:-1]

        if not german:
            l5_repl = {'STOWN': 'SAWON', 'MPSON': 'MASON'}
            l4_repl = {
                'NSEN': 'ASEN',
                'MSON': 'ASON',
                'STEN': 'SAEN',
                'STON': 'SAON',
            }
            if lname[-5:] in l5_repl:
                lname = lname[:-5] + l5_repl[lname[-5:]]
            elif lname[-4:] in l4_repl:
                lname = lname[:-4] + l4_repl[lname[-4:]]

        if lname[-2:] in {'NG', 'ND'}:
            lname = lname[:-1]
        if not german and lname[-3:] in {'GAN', 'GEN'}:
            lname = lname[:-3] + 'A' + lname[-2:]

        # C. Infix Treatment
        lname = lname.replace('CK', 'C')
        lname = lname.replace('SCH', 'S')
        lname = lname.replace('DT', 'T')
        lname = lname.replace('ND', 'N')
        lname = lname.replace('NG', 'N')
        lname = lname.replace('LM', 'M')
        lname = lname.replace('MN', 'M')
        lname = lname.replace('WIE', 'VIE')
        lname = lname.replace('WEI', 'VEI')

        # D. Soundexing
        # code for X & Y are unspecified, but presumably are 2 & 0

        lname = lname.translate(self._trans)
        lname = self._delete_consecutive_repeats(lname)

        code += lname[1:]
        code = code.replace('0', '')  # rule 1

        if max_length != -1:
            if len(code) < max_length:
                code += '0' * (max_length - len(code))
            else:
                code = code[:max_length]

        return code