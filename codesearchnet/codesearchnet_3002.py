def ProcessFile(filename, vlevel, extra_check_functions=None):
  """Does google-lint on a single file.

  Args:
    filename: The name of the file to parse.

    vlevel: The level of errors to report.  Every error of confidence
    >= verbose_level will be reported.  0 is a good default.

    extra_check_functions: An array of additional check functions that will be
                           run on each source line. Each function takes 4
                           arguments: filename, clean_lines, line, error
  """

  _SetVerboseLevel(vlevel)
  _BackupFilters()

  if not ProcessConfigOverrides(filename):
    _RestoreFilters()
    return

  lf_lines = []
  crlf_lines = []
  try:
    # Support the UNIX convention of using "-" for stdin.  Note that
    # we are not opening the file with universal newline support
    # (which codecs doesn't support anyway), so the resulting lines do
    # contain trailing '\r' characters if we are reading a file that
    # has CRLF endings.
    # If after the split a trailing '\r' is present, it is removed
    # below.
    if filename == '-':
      lines = codecs.StreamReaderWriter(sys.stdin,
                                        codecs.getreader('utf8'),
                                        codecs.getwriter('utf8'),
                                        'replace').read().split('\n')
    else:
      lines = codecs.open(filename, 'r', 'utf8', 'replace').read().split('\n')

    # Remove trailing '\r'.
    # The -1 accounts for the extra trailing blank line we get from split()
    for linenum in range(len(lines) - 1):
      if lines[linenum].endswith('\r'):
        lines[linenum] = lines[linenum].rstrip('\r')
        crlf_lines.append(linenum + 1)
      else:
        lf_lines.append(linenum + 1)

  except IOError:
    _cpplint_state.PrintError(
        "Skipping input '%s': Can't open for reading\n" % filename)
    _RestoreFilters()
    return

  # Note, if no dot is found, this will give the entire filename as the ext.
  file_extension = filename[filename.rfind('.') + 1:]

  # When reading from stdin, the extension is unknown, so no cpplint tests
  # should rely on the extension.
  if filename != '-' and file_extension not in GetAllExtensions():
    # bazel 0.5.1> uses four distinct generated files that gives a warning
    # we suppress the warning for these files
    bazel_gen_files = set([ 
        "external/local_config_cc/libtool",
        "external/local_config_cc/make_hashed_objlist.py", 
        "external/local_config_cc/wrapped_ar",
        "external/local_config_cc/wrapped_clang",
        "external/local_config_cc/xcrunwrapper.sh",
    ])
    if not filename in bazel_gen_files:
       _cpplint_state.PrintError('Ignoring %s; not a valid file name '
                                 '(%s)\n' % (filename, ', '.join(GetAllExtensions())))
  else:
    ProcessFileData(filename, file_extension, lines, Error,
                    extra_check_functions)

    # If end-of-line sequences are a mix of LF and CR-LF, issue
    # warnings on the lines with CR.
    #
    # Don't issue any warnings if all lines are uniformly LF or CR-LF,
    # since critique can handle these just fine, and the style guide
    # doesn't dictate a particular end of line sequence.
    #
    # We can't depend on os.linesep to determine what the desired
    # end-of-line sequence should be, since that will return the
    # server-side end-of-line sequence.
    if lf_lines and crlf_lines:
      # Warn on every line with CR.  An alternative approach might be to
      # check whether the file is mostly CRLF or just LF, and warn on the
      # minority, we bias toward LF here since most tools prefer LF.
      for linenum in crlf_lines:
        Error(filename, linenum, 'whitespace/newline', 1,
              'Unexpected \\r (^M) found; better to use only \\n')

  _RestoreFilters()