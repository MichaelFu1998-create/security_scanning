def _ClassifyInclude(fileinfo, include, is_system):
  """Figures out what kind of header 'include' is.

  Args:
    fileinfo: The current file cpplint is running over. A FileInfo instance.
    include: The path to a #included file.
    is_system: True if the #include used <> rather than "".

  Returns:
    One of the _XXX_HEADER constants.

  For example:
    >>> _ClassifyInclude(FileInfo('foo/foo.cc'), 'stdio.h', True)
    _C_SYS_HEADER
    >>> _ClassifyInclude(FileInfo('foo/foo.cc'), 'string', True)
    _CPP_SYS_HEADER
    >>> _ClassifyInclude(FileInfo('foo/foo.cc'), 'foo/foo.h', False)
    _LIKELY_MY_HEADER
    >>> _ClassifyInclude(FileInfo('foo/foo_unknown_extension.cc'),
    ...                  'bar/foo_other_ext.h', False)
    _POSSIBLE_MY_HEADER
    >>> _ClassifyInclude(FileInfo('foo/foo.cc'), 'foo/bar.h', False)
    _OTHER_HEADER
  """
  # This is a list of all standard c++ header files, except
  # those already checked for above.
  is_cpp_h = include in _CPP_HEADERS

  # Headers with C++ extensions shouldn't be considered C system headers
  if is_system and os.path.splitext(include)[1] in ['.hpp', '.hxx', '.h++']:
      is_system = False

  if is_system:
    if is_cpp_h:
      return _CPP_SYS_HEADER
    else:
      return _C_SYS_HEADER

  # If the target file and the include we're checking share a
  # basename when we drop common extensions, and the include
  # lives in . , then it's likely to be owned by the target file.
  target_dir, target_base = (
      os.path.split(_DropCommonSuffixes(fileinfo.RepositoryName())))
  include_dir, include_base = os.path.split(_DropCommonSuffixes(include))
  target_dir_pub = os.path.normpath(target_dir + '/../public')
  target_dir_pub = target_dir_pub.replace('\\', '/')
  if target_base == include_base and (
      include_dir == target_dir or
      include_dir == target_dir_pub):
    return _LIKELY_MY_HEADER

  # If the target and include share some initial basename
  # component, it's possible the target is implementing the
  # include, so it's allowed to be first, but we'll never
  # complain if it's not there.
  target_first_component = _RE_FIRST_COMPONENT.match(target_base)
  include_first_component = _RE_FIRST_COMPONENT.match(include_base)
  if (target_first_component and include_first_component and
      target_first_component.group(0) ==
      include_first_component.group(0)):
    return _POSSIBLE_MY_HEADER

  return _OTHER_HEADER