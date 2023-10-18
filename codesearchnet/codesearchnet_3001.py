def ProcessConfigOverrides(filename):
  """ Loads the configuration files and processes the config overrides.

  Args:
    filename: The name of the file being processed by the linter.

  Returns:
    False if the current |filename| should not be processed further.
  """

  abs_filename = os.path.abspath(filename)
  cfg_filters = []
  keep_looking = True
  while keep_looking:
    abs_path, base_name = os.path.split(abs_filename)
    if not base_name:
      break  # Reached the root directory.

    cfg_file = os.path.join(abs_path, "CPPLINT.cfg")
    abs_filename = abs_path
    if not os.path.isfile(cfg_file):
      continue

    try:
      with open(cfg_file) as file_handle:
        for line in file_handle:
          line, _, _ = line.partition('#')  # Remove comments.
          if not line.strip():
            continue

          name, _, val = line.partition('=')
          name = name.strip()
          val = val.strip()
          if name == 'set noparent':
            keep_looking = False
          elif name == 'filter':
            cfg_filters.append(val)
          elif name == 'exclude_files':
            # When matching exclude_files pattern, use the base_name of
            # the current file name or the directory name we are processing.
            # For example, if we are checking for lint errors in /foo/bar/baz.cc
            # and we found the .cfg file at /foo/CPPLINT.cfg, then the config
            # file's "exclude_files" filter is meant to be checked against "bar"
            # and not "baz" nor "bar/baz.cc".
            if base_name:
              pattern = re.compile(val)
              if pattern.match(base_name):
                _cpplint_state.PrintInfo('Ignoring "%s": file excluded by '
                    '"%s". File path component "%s" matches pattern "%s"\n' %
                    (filename, cfg_file, base_name, val))
                return False
          elif name == 'linelength':
            global _line_length
            try:
                _line_length = int(val)
            except ValueError:
                _cpplint_state.PrintError('Line length must be numeric.')
          elif name == 'extensions':
              global _valid_extensions
              try:
                  extensions = [ext.strip() for ext in val.split(',')]
                  _valid_extensions = set(extensions)
              except ValueError:
                  sys.stderr.write('Extensions should be a comma-separated list of values;'
                                   'for example: extensions=hpp,cpp\n'
                                   'This could not be parsed: "%s"' % (val,))
          elif name == 'headers':
              global _header_extensions
              try:
                  extensions = [ext.strip() for ext in val.split(',')]
                  _header_extensions = set(extensions)
              except ValueError:
                  sys.stderr.write('Extensions should be a comma-separated list of values;'
                                   'for example: extensions=hpp,cpp\n'
                                   'This could not be parsed: "%s"' % (val,))
          elif name == 'root':
            global _root
            _root = val
          else:
            _cpplint_state.PrintError(
                'Invalid configuration option (%s) in file %s\n' %
                (name, cfg_file))

    except IOError:
      _cpplint_state.PrintError(
          "Skipping config file '%s': Can't open for reading\n" % cfg_file)
      keep_looking = False

  # Apply all the accumulated filters in reverse order (top-level directory
  # config options having the least priority).
  for cfg_filter in reversed(cfg_filters):
     _AddFilters(cfg_filter)

  return True