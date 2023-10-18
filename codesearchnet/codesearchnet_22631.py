def FromJsonString(self, value):
    """Converts a string to Duration.

    Args:
      value: A string to be converted. The string must end with 's'. Any
          fractional digits (or none) are accepted as long as they fit into
          precision. For example: "1s", "1.01s", "1.0000001s", "-3.100s

    Raises:
      ParseError: On parsing problems.
    """
    if len(value) < 1 or value[-1] != 's':
      raise ParseError(
          'Duration must end with letter "s": {0}.'.format(value))
    try:
      pos = value.find('.')
      if pos == -1:
        self.seconds = int(value[:-1])
        self.nanos = 0
      else:
        self.seconds = int(value[:pos])
        if value[0] == '-':
          self.nanos = int(round(float('-0{0}'.format(value[pos: -1])) *1e9))
        else:
          self.nanos = int(round(float('0{0}'.format(value[pos: -1])) *1e9))
    except ValueError:
      raise ParseError(
          'Couldn\'t parse duration: {0}.'.format(value))