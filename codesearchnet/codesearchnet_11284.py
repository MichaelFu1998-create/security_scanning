def fingerprint(self, phrase, joiner=' '):
        """Return string fingerprint.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the fingerprint
        joiner : str
            The string that will be placed between each word

        Returns
        -------
        str
            The fingerprint of the phrase

        Example
        -------
        >>> sf = String()
        >>> sf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'brown dog fox jumped lazy over quick the'

        """
        phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
        phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
        phrase = joiner.join(sorted(list(set(phrase.split()))))
        return phrase