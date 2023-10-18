def encode(self, lname, fname='.', omit_fname=False):
        """Return Davidson's Consonant Code.

        Parameters
        ----------
        lname : str
            Last name (or word) to be encoded
        fname : str
            First name (optional), of which the first character is included in
            the code.
        omit_fname : bool
            Set to True to completely omit the first character of the first
            name

        Returns
        -------
        str
            Davidson's Consonant Code

        Example
        -------
        >>> pe = Davidson()
        >>> pe.encode('Gough')
        'G   .'
        >>> pe.encode('pneuma')
        'PNM .'
        >>> pe.encode('knight')
        'KNGT.'
        >>> pe.encode('trice')
        'TRC .'
        >>> pe.encode('judge')
        'JDG .'
        >>> pe.encode('Smith', 'James')
        'SMT J'
        >>> pe.encode('Wasserman', 'Tabitha')
        'WSRMT'

        """
        lname = text_type(lname.upper())
        code = self._delete_consecutive_repeats(
            lname[:1] + lname[1:].translate(self._trans)
        )
        code = code[:4] + (4 - len(code)) * ' '

        if not omit_fname:
            code += fname[:1].upper()

        return code