def CheckIncludeLine(filename, clean_lines, linenum, include_state, error):
  """Check rules that are applicable to #include lines.

  Strings on #include lines are NOT removed from elided line, to make
  certain tasks easier. However, to prevent false positives, checks
  applicable to #include lines in CheckLanguage must be put here.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    include_state: An _IncludeState instance in which the headers are inserted.
    error: The function to call with any errors found.
  """
  fileinfo = FileInfo(filename)
  line = clean_lines.lines[linenum]

  # "include" should use the new style "foo/bar.h" instead of just "bar.h"
  # Only do this check if the included header follows google naming
  # conventions.  If not, assume that it's a 3rd party API that
  # requires special include conventions.
  #
  # We also make an exception for Lua headers, which follow google
  # naming convention but not the include convention.
  match = Match(r'#include\s*"([^/]+\.h)"', line)
  if match and not _THIRD_PARTY_HEADERS_PATTERN.match(match.group(1)):
    error(filename, linenum, 'build/include_subdir', 4,
          'Include the directory when naming .h files')

  # we shouldn't include a file more than once. actually, there are a
  # handful of instances where doing so is okay, but in general it's
  # not.
  match = _RE_PATTERN_INCLUDE.search(line)
  if match:
    include = match.group(2)
    is_system = (match.group(1) == '<')
    duplicate_line = include_state.FindHeader(include)
    if duplicate_line >= 0:
      error(filename, linenum, 'build/include', 4,
            '"%s" already included at %s:%s' %
            (include, filename, duplicate_line))
      return

    for extension in GetNonHeaderExtensions():
      if (include.endswith('.' + extension) and
          os.path.dirname(fileinfo.RepositoryName()) != os.path.dirname(include)):
        error(filename, linenum, 'build/include', 4,
              'Do not include .' + extension + ' files from other packages')
        return

    if not _THIRD_PARTY_HEADERS_PATTERN.match(include):
      include_state.include_list[-1].append((include, linenum))

      # We want to ensure that headers appear in the right order:
      # 1) for foo.cc, foo.h  (preferred location)
      # 2) c system files
      # 3) cpp system files
      # 4) for foo.cc, foo.h  (deprecated location)
      # 5) other google headers
      #
      # We classify each include statement as one of those 5 types
      # using a number of techniques. The include_state object keeps
      # track of the highest type seen, and complains if we see a
      # lower type after that.
      error_message = include_state.CheckNextIncludeOrder(
          _ClassifyInclude(fileinfo, include, is_system))
      if error_message:
        error(filename, linenum, 'build/include_order', 4,
              '%s. Should be: %s.h, c system, c++ system, other.' %
              (error_message, fileinfo.BaseName()))
      canonical_include = include_state.CanonicalizeAlphabeticalOrder(include)
      if not include_state.IsInAlphabeticalOrder(
          clean_lines, linenum, canonical_include):
        error(filename, linenum, 'build/include_alpha', 4,
              'Include "%s" not in alphabetical order' % include)
      include_state.SetLastHeader(canonical_include)