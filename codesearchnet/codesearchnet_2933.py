def IsErrorSuppressedByNolint(category, linenum):
  """Returns true if the specified error category is suppressed on this line.

  Consults the global error_suppressions map populated by
  ParseNolintSuppressions/ProcessGlobalSuppresions/ResetNolintSuppressions.

  Args:
    category: str, the category of the error.
    linenum: int, the current line number.
  Returns:
    bool, True iff the error should be suppressed due to a NOLINT comment or
    global suppression.
  """
  return (_global_error_suppressions.get(category, False) or
          linenum in _error_suppressions.get(category, set()) or
          linenum in _error_suppressions.get(None, set()))