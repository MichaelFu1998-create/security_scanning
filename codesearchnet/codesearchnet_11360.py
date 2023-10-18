def encode(self, word, max_length=4, zero_pad=True):
        """Return the Phonex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Phonex value

        Examples
        --------
        >>> pe = Phonex()
        >>> pe.encode('Christopher')
        'C623'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Schmidt')
        'S253'
        >>> pe.encode('Smith')
        'S530'

        """
        name = unicode_normalize('NFKD', text_type(word.upper()))
        name = name.replace('�', 'SS')

        # Clamp max_length to [4, 64]
        if max_length != -1:
            max_length = min(max(4, max_length), 64)
        else:
            max_length = 64

        name_code = last = ''

        # Deletions effected by replacing with next letter which
        # will be ignored due to duplicate handling of Soundex code.
        # This is faster than 'moving' all subsequent letters.

        # Remove any trailing Ss
        while name[-1:] == 'S':
            name = name[:-1]

        # Phonetic equivalents of first 2 characters
        # Works since duplicate letters are ignored
        if name[:2] == 'KN':
            name = 'N' + name[2:]  # KN.. == N..
        elif name[:2] == 'PH':
            name = 'F' + name[2:]  # PH.. == F.. (H ignored anyway)
        elif name[:2] == 'WR':
            name = 'R' + name[2:]  # WR.. == R..

        if name:
            # Special case, ignore H first letter (subsequent Hs ignored
            # anyway)
            # Works since duplicate letters are ignored
            if name[0] == 'H':
                name = name[1:]

        if name:
            # Phonetic equivalents of first character
            if name[0] in self._uc_vy_set:
                name = 'A' + name[1:]
            elif name[0] in {'B', 'P'}:
                name = 'B' + name[1:]
            elif name[0] in {'V', 'F'}:
                name = 'F' + name[1:]
            elif name[0] in {'C', 'K', 'Q'}:
                name = 'C' + name[1:]
            elif name[0] in {'G', 'J'}:
                name = 'G' + name[1:]
            elif name[0] in {'S', 'Z'}:
                name = 'S' + name[1:]

            name_code = last = name[0]

        # Modified Soundex code
        for i in range(1, len(name)):
            code = '0'
            if name[i] in {'B', 'F', 'P', 'V'}:
                code = '1'
            elif name[i] in {'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z'}:
                code = '2'
            elif name[i] in {'D', 'T'}:
                if name[i + 1 : i + 2] != 'C':
                    code = '3'
            elif name[i] == 'L':
                if name[i + 1 : i + 2] in self._uc_vy_set or i + 1 == len(
                    name
                ):
                    code = '4'
            elif name[i] in {'M', 'N'}:
                if name[i + 1 : i + 2] in {'D', 'G'}:
                    name = name[: i + 1] + name[i] + name[i + 2 :]
                code = '5'
            elif name[i] == 'R':
                if name[i + 1 : i + 2] in self._uc_vy_set or i + 1 == len(
                    name
                ):
                    code = '6'

            if code != last and code != '0' and i != 0:
                name_code += code

            last = name_code[-1]

        if zero_pad:
            name_code += '0' * max_length
        if not name_code:
            name_code = '0'
        return name_code[:max_length]