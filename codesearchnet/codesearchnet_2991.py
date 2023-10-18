def ExpectingFunctionArgs(clean_lines, linenum):
  """Checks whether where function type arguments are expected.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.

  Returns:
    True if the line at 'linenum' is inside something that expects arguments
    of function types.
  """
  line = clean_lines.elided[linenum]
  return (Match(r'^\s*MOCK_(CONST_)?METHOD\d+(_T)?\(', line) or
          (linenum >= 2 and
           (Match(r'^\s*MOCK_(?:CONST_)?METHOD\d+(?:_T)?\((?:\S+,)?\s*$',
                  clean_lines.elided[linenum - 1]) or
            Match(r'^\s*MOCK_(?:CONST_)?METHOD\d+(?:_T)?\(\s*$',
                  clean_lines.elided[linenum - 2]) or
            Search(r'\bstd::m?function\s*\<\s*$',
                   clean_lines.elided[linenum - 1]))))