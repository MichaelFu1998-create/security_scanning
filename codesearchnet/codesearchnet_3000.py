def ProcessFileData(filename, file_extension, lines, error,
                    extra_check_functions=None):
  """Performs lint checks and reports any errors to the given error function.

  Args:
    filename: Filename of the file that is being processed.
    file_extension: The extension (dot not included) of the file.
    lines: An array of strings, each representing a line of the file, with the
           last element being empty if the file is terminated with a newline.
    error: A callable to which errors are reported, which takes 4 arguments:
           filename, line number, error level, and message
    extra_check_functions: An array of additional check functions that will be
                           run on each source line. Each function takes 4
                           arguments: filename, clean_lines, line, error
  """
  lines = (['// marker so line numbers and indices both start at 1'] + lines +
           ['// marker so line numbers end in a known way'])

  include_state = _IncludeState()
  function_state = _FunctionState()
  nesting_state = NestingState()

  ResetNolintSuppressions()

  CheckForCopyright(filename, lines, error)
  ProcessGlobalSuppresions(lines)
  RemoveMultiLineComments(filename, lines, error)
  clean_lines = CleansedLines(lines)

  if file_extension in GetHeaderExtensions():
    CheckForHeaderGuard(filename, clean_lines, error)

  for line in range(clean_lines.NumLines()):
    ProcessLine(filename, file_extension, clean_lines, line,
                include_state, function_state, nesting_state, error,
                extra_check_functions)
    FlagCxx11Features(filename, clean_lines, line, error)
  nesting_state.CheckCompletedBlocks(filename, error)

  CheckForIncludeWhatYouUse(filename, clean_lines, include_state, error)

  # Check that the .cc file has included its header if it exists.
  if _IsSourceExtension(file_extension):
    CheckHeaderFileIncluded(filename, include_state, error)

  # We check here rather than inside ProcessLine so that we see raw
  # lines rather than "cleaned" lines.
  CheckForBadCharacters(filename, lines, error)

  CheckForNewlineAtEOF(filename, lines, error)