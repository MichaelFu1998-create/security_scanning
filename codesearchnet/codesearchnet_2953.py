def CheckHeaderFileIncluded(filename, include_state, error):
  """Logs an error if a source file does not include its header."""

  # Do not check test files
  fileinfo = FileInfo(filename)
  if Search(_TEST_FILE_SUFFIX, fileinfo.BaseName()):
    return

  for ext in GetHeaderExtensions():
      basefilename = filename[0:len(filename) - len(fileinfo.Extension())]
      headerfile = basefilename + '.' + ext
      if not os.path.exists(headerfile):
        continue
      headername = FileInfo(headerfile).RepositoryName()
      first_include = None
      for section_list in include_state.include_list:
        for f in section_list:
          if headername in f[0] or f[0] in headername:
            return
          if not first_include:
            first_include = f[1]

      error(filename, first_include, 'build/include', 5,
            '%s should include its header file %s' % (fileinfo.RepositoryName(),
                                                      headername))