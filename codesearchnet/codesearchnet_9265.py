def outputs_are_present(outputs):
  """True if each output contains at least one file or no output specified."""
  # outputs are OutputFileParam (see param_util.py)

  # If outputs contain a pattern, then there is no way for `dsub` to verify
  # that *all* output is present. The best that `dsub` can do is to verify
  # that *some* output was created for each such parameter.
  for o in outputs:
    if not o.value:
      continue
    if o.recursive:
      if not folder_exists(o.value):
        return False
    else:
      if not simple_pattern_exists_in_gcs(o.value):
        return False
  return True