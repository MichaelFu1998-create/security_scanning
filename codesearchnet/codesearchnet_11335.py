def encode(self, word, lang='en'):
        """Return the MetaSoundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        lang : str
            Either ``en`` for English or ``es`` for Spanish

        Returns
        -------
        str
            The MetaSoundex code

        Examples
        --------
        >>> pe = MetaSoundex()
        >>> pe.encode('Smith')
        '4500'
        >>> pe.encode('Waters')
        '7362'
        >>> pe.encode('James')
        '1520'
        >>> pe.encode('Schmidt')
        '4530'
        >>> pe.encode('Ashcroft')
        '0261'
        >>> pe.encode('Perez', lang='es')
        '094'
        >>> pe.encode('Martinez', lang='es')
        '69364'
        >>> pe.encode('Gutierrez', lang='es')
        '83994'
        >>> pe.encode('Santiago', lang='es')
        '4638'
        >>> pe.encode('Nicolás', lang='es')
        '6754'

        """
        if lang == 'es':
            return self._phonetic_spanish.encode(
                self._spanish_metaphone.encode(word)
            )

        word = self._soundex.encode(self._metaphone.encode(word))
        word = word[0].translate(self._trans) + word[1:]
        return word