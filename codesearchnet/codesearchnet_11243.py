def _to_alpha(self, num):
        """Convert a Kölner Phonetik code from numeric to alphabetic.

        Parameters
        ----------
        num : str or int
            A numeric Kölner Phonetik representation

        Returns
        -------
        str
            An alphabetic representation of the same word

        Examples
        --------
        >>> pe = Koelner()
        >>> pe._to_alpha('862')
        'SNT'
        >>> pe._to_alpha('657')
        'NLR'
        >>> pe._to_alpha('86766')
        'SNRNN'

        """
        num = ''.join(c for c in text_type(num) if c in self._num_set)
        return num.translate(self._num_trans)