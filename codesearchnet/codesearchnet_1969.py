def next(self, eof_token=False):
        """
        Returns token at ``offset`` as a :class:`Token` and advances ``offset``
        to point past the end of the token, where the token has:

        - *range* which is a :class:`pythonparser.source.Range` that includes
          the token but not surrounding whitespace,
        - *kind* which is a string containing one of Python keywords or operators,
          ``newline``, ``float``, ``int``, ``complex``, ``strbegin``,
          ``strdata``, ``strend``, ``ident``, ``indent``, ``dedent`` or ``eof``
          (if ``eof_token`` is True).
        - *value* which is the flags as lowercase string if *kind* is ``strbegin``,
          the string contents if *kind* is ``strdata``,
          the numeric value if *kind* is ``float``, ``int`` or ``complex``,
          the identifier if *kind* is ``ident`` and ``None`` in any other case.

        :param eof_token: if true, will return a token with kind ``eof``
            when the input is exhausted; if false, will raise ``StopIteration``.
        """
        if len(self.queue) == 0:
            self._refill(eof_token)

        return self.queue.pop(0)