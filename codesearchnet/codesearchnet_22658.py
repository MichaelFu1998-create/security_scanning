def _ParseOrMerge(self, lines, message):
    """Converts an text representation of a protocol message into a message.

    Args:
      lines: Lines of a message's text representation.
      message: A protocol buffer message to merge into.

    Raises:
      ParseError: On text parsing problems.
    """
    tokenizer = _Tokenizer(lines)
    while not tokenizer.AtEnd():
      self._MergeField(tokenizer, message)