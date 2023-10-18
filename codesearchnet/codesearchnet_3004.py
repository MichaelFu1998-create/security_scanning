def ParseArguments(args):
  """Parses the command line arguments.

  This may set the output format and verbosity level as side-effects.

  Args:
    args: The command line arguments:

  Returns:
    The list of filenames to lint.
  """
  try:
    (opts, filenames) = getopt.getopt(args, '', ['help', 'output=', 'verbose=',
                                                 'counting=',
                                                 'filter=',
                                                 'root=',
                                                 'repository=',
                                                 'linelength=',
                                                 'extensions=',
                                                 'exclude=',
                                                 'headers=',
                                                 'quiet',
                                                 'recursive'])
  except getopt.GetoptError:
    PrintUsage('Invalid arguments.')

  verbosity = _VerboseLevel()
  output_format = _OutputFormat()
  filters = ''
  counting_style = ''
  recursive = False

  for (opt, val) in opts:
    if opt == '--help':
      PrintUsage(None)
    elif opt == '--output':
      if val not in ('emacs', 'vs7', 'eclipse', 'junit'):
        PrintUsage('The only allowed output formats are emacs, vs7, eclipse '
                   'and junit.')
      output_format = val
    elif opt == '--verbose':
      verbosity = int(val)
    elif opt == '--filter':
      filters = val
      if not filters:
        PrintCategories()
    elif opt == '--counting':
      if val not in ('total', 'toplevel', 'detailed'):
        PrintUsage('Valid counting options are total, toplevel, and detailed')
      counting_style = val
    elif opt == '--root':
      global _root
      _root = val
    elif opt == '--repository':
      global _repository
      _repository = val
    elif opt == '--linelength':
      global _line_length
      try:
        _line_length = int(val)
      except ValueError:
        PrintUsage('Line length must be digits.')
    elif opt == '--exclude':
      global _excludes
      if not _excludes:
        _excludes = set()
      _excludes.update(glob.glob(val))
    elif opt == '--extensions':
      global _valid_extensions
      try:
        _valid_extensions = set(val.split(','))
      except ValueError:
          PrintUsage('Extensions must be comma seperated list.')
    elif opt == '--headers':
      global _header_extensions
      try:
          _header_extensions = set(val.split(','))
      except ValueError:
        PrintUsage('Extensions must be comma seperated list.')
    elif opt == '--recursive':
      recursive = True
    elif opt == '--quiet':
      global _quiet
      _quiet = True

  if not filenames:
    PrintUsage('No files were specified.')

  if recursive:
    filenames = _ExpandDirectories(filenames)

  if _excludes:
    filenames = _FilterExcludedFiles(filenames)

  _SetOutputFormat(output_format)
  _SetVerboseLevel(verbosity)
  _SetFilters(filters)
  _SetCountingStyle(counting_style)

  return filenames