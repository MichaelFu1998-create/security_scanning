def GetHeaderGuardCPPVariable(filename):
  """Returns the CPP variable that should be used as a header guard.

  Args:
    filename: The name of a C++ header file.

  Returns:
    The CPP variable that should be used as a header guard in the
    named file.

  """

  # Restores original filename in case that cpplint is invoked from Emacs's
  # flymake.
  filename = re.sub(r'_flymake\.h$', '.h', filename)
  filename = re.sub(r'/\.flymake/([^/]*)$', r'/\1', filename)
  # Replace 'c++' with 'cpp'.
  filename = filename.replace('C++', 'cpp').replace('c++', 'cpp')

  fileinfo = FileInfo(filename)
  file_path_from_root = fileinfo.RepositoryName()
  if _root:
    suffix = os.sep
    # On Windows using directory separator will leave us with
    # "bogus escape error" unless we properly escape regex.
    if suffix == '\\':
      suffix += '\\'
    file_path_from_root = re.sub('^' + _root + suffix, '', file_path_from_root)
  return re.sub(r'[^a-zA-Z0-9]', '_', file_path_from_root).upper() + '_'