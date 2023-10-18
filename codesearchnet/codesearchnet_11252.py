def encode(self, word, max_length=4):
        """Return the SoundD code.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)

        Returns
        -------
        str
            The SoundD code

        Examples
        --------
        >>> sound_d('Gough')
        '2000'
        >>> sound_d('pneuma')
        '5500'
        >>> sound_d('knight')
        '5300'
        >>> sound_d('trice')
        '3620'
        >>> sound_d('judge')
        '2200'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        if word[:2] in {'KN', 'GN', 'PN', 'AC', 'WR'}:
            word = word[1:]
        elif word[:1] == 'X':
            word = 'S' + word[1:]
        elif word[:2] == 'WH':
            word = 'W' + word[2:]

        word = (
            word.replace('DGE', '20').replace('DGI', '20').replace('GH', '0')
        )

        word = word.translate(self._trans)
        word = self._delete_consecutive_repeats(word)
        word = word.replace('0', '')

        if max_length != -1:
            if len(word) < max_length:
                word += '0' * (max_length - len(word))
            else:
                word = word[:max_length]

        return word