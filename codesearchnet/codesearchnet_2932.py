def ProcessGlobalSuppresions(lines):
  """Updates the list of global error suppressions.

  Parses any lint directives in the file that have global effect.

  Args:
    lines: An array of strings, each representing a line of the file, with the
           last element being empty if the file is terminated with a newline.
  """
  for line in lines:
    if _SEARCH_C_FILE.search(line):
      for category in _DEFAULT_C_SUPPRESSED_CATEGORIES:
        _global_error_suppressions[category] = True
    if _SEARCH_KERNEL_FILE.search(line):
      for category in _DEFAULT_KERNEL_SUPPRESSED_CATEGORIES:
        _global_error_suppressions[category] = True