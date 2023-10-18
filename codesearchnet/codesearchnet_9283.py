def _convert_suffix_to_docker_chars(suffix):
  """Rewrite string so that all characters are valid in a docker name suffix."""
  # Docker container names must match: [a-zA-Z0-9][a-zA-Z0-9_.-]
  accepted_characters = string.ascii_letters + string.digits + '_.-'

  def label_char_transform(char):
    if char in accepted_characters:
      return char
    return '-'

  return ''.join(label_char_transform(c) for c in suffix)