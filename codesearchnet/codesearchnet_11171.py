def encode(self, word, max_length=14):
        """Return the IBM Alpha Search Inquiry System code for a word.

        A collection is necessary as the return type since there can be
        multiple values for a single word. But the collection must be ordered
        since the first value is the primary coding.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 14)

        Returns
        -------
        tuple
            The Alpha-SIS value

        Examples
        --------
        >>> pe = AlphaSIS()
        >>> pe.encode('Christopher')
        ('06401840000000', '07040184000000', '04018400000000')
        >>> pe.encode('Niall')
        ('02500000000000',)
        >>> pe.encode('Smith')
        ('03100000000000',)
        >>> pe.encode('Schmidt')
        ('06310000000000',)

        """
        alpha = ['']
        pos = 0
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        # Clamp max_length to [4, 64]
        if max_length != -1:
            max_length = min(max(4, max_length), 64)
        else:
            max_length = 64

        # Do special processing for initial substrings
        for k in self._alpha_sis_initials_order:
            if word.startswith(k):
                alpha[0] += self._alpha_sis_initials[k]
                pos += len(k)
                break

        # Add a '0' if alpha is still empty
        if not alpha[0]:
            alpha[0] += '0'

        # Whether or not any special initial codes were encoded, iterate
        # through the length of the word in the main encoding loop
        while pos < len(word):
            orig_pos = pos
            for k in self._alpha_sis_basic_order:
                if word[pos:].startswith(k):
                    if isinstance(self._alpha_sis_basic[k], tuple):
                        newalpha = []
                        for i in range(len(self._alpha_sis_basic[k])):
                            newalpha += [
                                _ + self._alpha_sis_basic[k][i] for _ in alpha
                            ]
                        alpha = newalpha
                    else:
                        alpha = [_ + self._alpha_sis_basic[k] for _ in alpha]
                    pos += len(k)
                    break
            if pos == orig_pos:
                alpha = [_ + '_' for _ in alpha]
                pos += 1

        # Trim doublets and placeholders
        for i in range(len(alpha)):
            pos = 1
            while pos < len(alpha[i]):
                if alpha[i][pos] == alpha[i][pos - 1]:
                    alpha[i] = alpha[i][:pos] + alpha[i][pos + 1 :]
                pos += 1
        alpha = (_.replace('_', '') for _ in alpha)

        # Trim codes and return tuple
        alpha = ((_ + ('0' * max_length))[:max_length] for _ in alpha)
        return tuple(alpha)