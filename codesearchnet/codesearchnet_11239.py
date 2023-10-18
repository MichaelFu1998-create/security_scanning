def encode(self, word, max_length=8):
        """Return the eudex phonetic hash of a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length in bits of the code returned (default 8)

        Returns
        -------
        int
            The eudex hash

        Examples
        --------
        >>> pe = Eudex()
        >>> pe.encode('Colin')
        432345564238053650
        >>> pe.encode('Christopher')
        433648490138894409
        >>> pe.encode('Niall')
        648518346341351840
        >>> pe.encode('Smith')
        720575940412906756
        >>> pe.encode('Schmidt')
        720589151732307997

        """
        # Lowercase input & filter unknown characters
        word = ''.join(
            char for char in word.lower() if char in self._initial_phones
        )

        if not word:
            word = '÷'

        # Perform initial eudex coding of each character
        values = [self._initial_phones[word[0]]]
        values += [self._trailing_phones[char] for char in word[1:]]

        # Right-shift by one to determine if second instance should be skipped
        shifted_values = [_ >> 1 for _ in values]
        condensed_values = [values[0]]
        for n in range(1, len(shifted_values)):
            if shifted_values[n] != shifted_values[n - 1]:
                condensed_values.append(values[n])

        # Add padding after first character & trim beyond max_length
        values = (
            [condensed_values[0]]
            + [0] * max(0, max_length - len(condensed_values))
            + condensed_values[1:max_length]
        )

        # Combine individual character values into eudex hash
        hash_value = 0
        for val in values:
            hash_value = (hash_value << 8) | val

        return hash_value