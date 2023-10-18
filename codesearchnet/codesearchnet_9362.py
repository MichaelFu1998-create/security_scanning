def convert_to_label_chars(s):
  """Turn the specified name and value into a valid Google label."""

  # We want the results to be user-friendly, not just functional.
  # So we can't base-64 encode it.
  #   * If upper-case: lower-case it
  #   * If the char is not a standard letter or digit. make it a dash

  # March 2019 note: underscores are now allowed in labels.
  # However, removing the conversion of underscores to dashes here would
  # create inconsistencies between old jobs and new jobs.
  # With existing code, $USER "jane_doe" has a user-id label of "jane-doe".
  # If we remove the conversion, the user-id label for new jobs is "jane_doe".
  # This makes looking up old jobs more complicated.

  accepted_characters = string.ascii_lowercase + string.digits + '-'

  def label_char_transform(char):
    if char in accepted_characters:
      return char
    if char in string.ascii_uppercase:
      return char.lower()
    return '-'

  return ''.join(label_char_transform(c) for c in s)