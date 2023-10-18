def CheckGlobalStatic(filename, clean_lines, linenum, error):
  """Check for unsafe global or static objects.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # Match two lines at a time to support multiline declarations
  if linenum + 1 < clean_lines.NumLines() and not Search(r'[;({]', line):
    line += clean_lines.elided[linenum + 1].strip()

  # Check for people declaring static/global STL strings at the top level.
  # This is dangerous because the C++ language does not guarantee that
  # globals with constructors are initialized before the first access, and
  # also because globals can be destroyed when some threads are still running.
  # TODO(unknown): Generalize this to also find static unique_ptr instances.
  # TODO(unknown): File bugs for clang-tidy to find these.
  match = Match(
      r'((?:|static +)(?:|const +))(?::*std::)?string( +const)? +'
      r'([a-zA-Z0-9_:]+)\b(.*)',
      line)

  # Remove false positives:
  # - String pointers (as opposed to values).
  #    string *pointer
  #    const string *pointer
  #    string const *pointer
  #    string *const pointer
  #
  # - Functions and template specializations.
  #    string Function<Type>(...
  #    string Class<Type>::Method(...
  #
  # - Operators.  These are matched separately because operator names
  #   cross non-word boundaries, and trying to match both operators
  #   and functions at the same time would decrease accuracy of
  #   matching identifiers.
  #    string Class::operator*()
  if (match and
      not Search(r'\bstring\b(\s+const)?\s*[\*\&]\s*(const\s+)?\w', line) and
      not Search(r'\boperator\W', line) and
      not Match(r'\s*(<.*>)?(::[a-zA-Z0-9_]+)*\s*\(([^"]|$)', match.group(4))):
    if Search(r'\bconst\b', line):
      error(filename, linenum, 'runtime/string', 4,
            'For a static/global string constant, use a C style string '
            'instead: "%schar%s %s[]".' %
            (match.group(1), match.group(2) or '', match.group(3)))
    else:
      error(filename, linenum, 'runtime/string', 4,
            'Static/global string variables are not permitted.')

  if (Search(r'\b([A-Za-z0-9_]*_)\(\1\)', line) or
      Search(r'\b([A-Za-z0-9_]*_)\(CHECK_NOTNULL\(\1\)\)', line)):
    error(filename, linenum, 'runtime/init', 4,
          'You seem to be initializing a member variable with itself.')