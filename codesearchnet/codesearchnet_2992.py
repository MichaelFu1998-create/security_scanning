def FilesBelongToSameModule(filename_cc, filename_h):
  """Check if these two filenames belong to the same module.

  The concept of a 'module' here is a as follows:
  foo.h, foo-inl.h, foo.cc, foo_test.cc and foo_unittest.cc belong to the
  same 'module' if they are in the same directory.
  some/path/public/xyzzy and some/path/internal/xyzzy are also considered
  to belong to the same module here.

  If the filename_cc contains a longer path than the filename_h, for example,
  '/absolute/path/to/base/sysinfo.cc', and this file would include
  'base/sysinfo.h', this function also produces the prefix needed to open the
  header. This is used by the caller of this function to more robustly open the
  header file. We don't have access to the real include paths in this context,
  so we need this guesswork here.

  Known bugs: tools/base/bar.cc and base/bar.h belong to the same module
  according to this implementation. Because of this, this function gives
  some false positives. This should be sufficiently rare in practice.

  Args:
    filename_cc: is the path for the source (e.g. .cc) file
    filename_h: is the path for the header path

  Returns:
    Tuple with a bool and a string:
    bool: True if filename_cc and filename_h belong to the same module.
    string: the additional prefix needed to open the header file.
  """
  fileinfo_cc = FileInfo(filename_cc)
  if not fileinfo_cc.Extension().lstrip('.') in GetNonHeaderExtensions():
    return (False, '')

  fileinfo_h = FileInfo(filename_h)
  if not fileinfo_h.Extension().lstrip('.') in GetHeaderExtensions():
    return (False, '')

  filename_cc = filename_cc[:-(len(fileinfo_cc.Extension()))]
  matched_test_suffix = Search(_TEST_FILE_SUFFIX, fileinfo_cc.BaseName())
  if matched_test_suffix:
    filename_cc = filename_cc[:-len(matched_test_suffix.group(1))]

  filename_cc = filename_cc.replace('/public/', '/')
  filename_cc = filename_cc.replace('/internal/', '/')

  filename_h = filename_h[:-(len(fileinfo_h.Extension()))]
  if filename_h.endswith('-inl'):
    filename_h = filename_h[:-len('-inl')]
  filename_h = filename_h.replace('/public/', '/')
  filename_h = filename_h.replace('/internal/', '/')

  files_belong_to_same_module = filename_cc.endswith(filename_h)
  common_path = ''
  if files_belong_to_same_module:
    common_path = filename_cc[:-len(filename_h)]
  return files_belong_to_same_module, common_path