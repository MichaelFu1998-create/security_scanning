def encode(self, word):
        """Return the Kölner Phonetik (numeric output) code for a word.

        While the output code is numeric, it is still a str because 0s can lead
        the code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Kölner Phonetik value as a numeric string

        Example
        -------
        >>> pe = Koelner()
        >>> pe.encode('Christopher')
        '478237'
        >>> pe.encode('Niall')
        '65'
        >>> pe.encode('Smith')
        '862'
        >>> pe.encode('Schmidt')
        '862'
        >>> pe.encode('Müller')
        '657'
        >>> pe.encode('Zimmermann')
        '86766'

        """

        def _after(word, pos, letters):
            """Return True if word[pos] follows one of the supplied letters.

            Parameters
            ----------
            word : str
                The word to check
            pos : int
                Position within word to check
            letters : str
                Letters to confirm precede word[pos]

            Returns
            -------
            bool
                True if word[pos] follows a value in letters

            """
            return pos > 0 and word[pos - 1] in letters

        def _before(word, pos, letters):
            """Return True if word[pos] precedes one of the supplied letters.

            Parameters
            ----------
            word : str
                The word to check
            pos : int
                Position within word to check
            letters : str
                Letters to confirm follow word[pos]

            Returns
            -------
            bool
                True if word[pos] precedes a value in letters

            """
            return pos + 1 < len(word) and word[pos + 1] in letters

        sdx = ''

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            return sdx

        for i in range(len(word)):
            if word[i] in self._uc_v_set:
                sdx += '0'
            elif word[i] == 'B':
                sdx += '1'
            elif word[i] == 'P':
                if _before(word, i, {'H'}):
                    sdx += '3'
                else:
                    sdx += '1'
            elif word[i] in {'D', 'T'}:
                if _before(word, i, {'C', 'S', 'Z'}):
                    sdx += '8'
                else:
                    sdx += '2'
            elif word[i] in {'F', 'V', 'W'}:
                sdx += '3'
            elif word[i] in {'G', 'K', 'Q'}:
                sdx += '4'
            elif word[i] == 'C':
                if _after(word, i, {'S', 'Z'}):
                    sdx += '8'
                elif i == 0:
                    if _before(
                        word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'}
                    ):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif word[i] == 'X':
                if _after(word, i, {'C', 'K', 'Q'}):
                    sdx += '8'
                else:
                    sdx += '48'
            elif word[i] == 'L':
                sdx += '5'
            elif word[i] in {'M', 'N'}:
                sdx += '6'
            elif word[i] == 'R':
                sdx += '7'
            elif word[i] in {'S', 'Z'}:
                sdx += '8'

        sdx = self._delete_consecutive_repeats(sdx)

        if sdx:
            sdx = sdx[:1] + sdx[1:].replace('0', '')

        return sdx