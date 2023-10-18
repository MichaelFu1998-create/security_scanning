def _ConsumeSingleByteString(self):
    """Consume one token of a string literal.

    String literals (whether bytes or text) can come in multiple adjacent
    tokens which are automatically concatenated, like in C or Python.  This
    method only consumes one token.

    Returns:
      The token parsed.
    Raises:
      ParseError: When the wrong format data is found.
    """
    text = self.token
    if len(text) < 1 or text[0] not in _QUOTES:
      raise self._ParseError('Expected string but found: %r' % (text,))

    if len(text) < 2 or text[-1] != text[0]:
      raise self._ParseError('String missing ending quote: %r' % (text,))

    try:
      result = text_encoding.CUnescape(text[1:-1])
    except ValueError as e:
      raise self._ParseError(str(e))
    self.NextToken()
    return result