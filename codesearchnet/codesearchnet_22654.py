def _SkipFieldValue(tokenizer):
  """Skips over a field value.

  Args:
    tokenizer: A tokenizer to parse the field name and values.

  Raises:
    ParseError: In case an invalid field value is found.
  """
  # String/bytes tokens can come in multiple adjacent string literals.
  # If we can consume one, consume as many as we can.
  if tokenizer.TryConsumeByteString():
    while tokenizer.TryConsumeByteString():
      pass
    return

  if (not tokenizer.TryConsumeIdentifier() and
      not tokenizer.TryConsumeInt64() and
      not tokenizer.TryConsumeUint64() and
      not tokenizer.TryConsumeFloat()):
    raise ParseError('Invalid field value: ' + tokenizer.token)