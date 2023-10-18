def split_pair(pair_string, separator, nullable_idx=1):
  """Split a string into a pair, which can have one empty value.

  Args:
    pair_string: The string to be split.
    separator: The separator to be used for splitting.
    nullable_idx: The location to be set to null if the separator is not in the
                  input string. Should be either 0 or 1.

  Returns:
    A list containing the pair.

  Raises:
    IndexError: If nullable_idx is not 0 or 1.
  """

  pair = pair_string.split(separator, 1)
  if len(pair) == 1:
    if nullable_idx == 0:
      return [None, pair[0]]
    elif nullable_idx == 1:
      return [pair[0], None]
    else:
      raise IndexError('nullable_idx should be either 0 or 1.')
  else:
    return pair