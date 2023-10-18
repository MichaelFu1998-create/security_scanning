def Parse(text, message):
  """Parses a JSON representation of a protocol message into a message.

  Args:
    text: Message JSON representation.
    message: A protocol beffer message to merge into.

  Returns:
    The same message passed as argument.

  Raises::
    ParseError: On JSON parsing problems.
  """
  if not isinstance(text, six.text_type): text = text.decode('utf-8')
  try:
    if sys.version_info < (2, 7):
      # object_pair_hook is not supported before python2.7
      js = json.loads(text)
    else:
      js = json.loads(text, object_pairs_hook=_DuplicateChecker)
  except ValueError as e:
    raise ParseError('Failed to load JSON: {0}.'.format(str(e)))
  _ConvertMessage(js, message)
  return message