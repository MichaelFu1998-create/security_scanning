def _remove_empty_items(d, required):
  """Return a new dict with any empty items removed.

  Note that this is not a deep check. If d contains a dictionary which
  itself contains empty items, those are never checked.

  This method exists to make to_serializable() functions cleaner.
  We could revisit this some day, but for now, the serialized objects are
  stripped of empty values to keep the output YAML more compact.

  Args:
    d: a dictionary
    required: list of required keys (for example, TaskDescriptors always emit
      the "task-id", even if None)

  Returns:
    A dictionary with empty items removed.
  """

  new_dict = {}
  for k, v in d.items():
    if k in required:
      new_dict[k] = v
    elif isinstance(v, int) or v:
      # "if v" would suppress emitting int(0)
      new_dict[k] = v

  return new_dict