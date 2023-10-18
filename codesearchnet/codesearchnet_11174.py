def fingerprint(self, phrase, qval=2, start_stop='', joiner=''):
        """Return Q-Gram fingerprint.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the q-gram fingerprint
        qval : int
            The length of each q-gram (by default 2)
        start_stop : str
            The start & stop symbol(s) to concatenate on either end of the
            phrase, as defined in :py:class:`tokenizer.QGrams`
        joiner : str
            The string that will be placed between each word

        Returns
        -------
        str
            The q-gram fingerprint of the phrase

        Examples
        --------
        >>> qf = QGram()
        >>> qf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
        >>> qf.fingerprint('Christopher')
        'cherhehrisopphristto'
        >>> qf.fingerprint('Niall')
        'aliallni'

        """
        phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
        phrase = ''.join(c for c in phrase if c.isalnum())
        phrase = QGrams(phrase, qval, start_stop)
        phrase = joiner.join(sorted(phrase))
        return phrase