def find_closing_braces(self, query):
    """Find the index of the closing braces for the opening braces
    at the start of the query string. Note that first character
    of input string must be an opening braces."""
    if query[0] != '(':
      raise Exception("Trying to find closing braces for no opening braces")
    num_open_braces = 0
    for i in range(len(query)):
      c = query[i]
      if c == '(':
        num_open_braces += 1
      elif c == ')':
        num_open_braces -= 1
      if num_open_braces == 0:
        return i
    raise Exception("No closing braces found")