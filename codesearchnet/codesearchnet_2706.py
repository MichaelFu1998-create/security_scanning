def parse_query_string(self, query):
    """Returns a parse tree for the query, each of the node is a
    subclass of Operator. This is both a lexical as well as syntax analyzer step."""
    if not query:
      return None
    # Just braces do not matter
    if query[0] == '(':
      index = self.find_closing_braces(query)
      # This must be the last index, since this was an NOP starting brace
      if index != len(query) - 1:
        raise Exception("Invalid syntax")
      else:
        return self.parse_query_string(query[1:-1])
    start_index = query.find("(")
    # There must be a ( in the query
    if start_index < 0:
      # Otherwise it must be a constant
      try:
        constant = float(query)
        return constant
      except ValueError:
        raise Exception("Invalid syntax")
    token = query[:start_index]
    if token not in self.operators:
      raise Exception("Invalid token: " + token)

    # Get sub components
    rest_of_the_query = query[start_index:]
    braces_end_index = self.find_closing_braces(rest_of_the_query)
    if braces_end_index != len(rest_of_the_query) - 1:
      raise Exception("Invalid syntax")
    parts = self.get_sub_parts(rest_of_the_query[1:-1])

    # parts are simple strings in this case
    if token == "TS":
      # This will raise exception if parts are not syntactically correct
      return self.operators[token](parts)

    children = []
    for part in parts:
      children.append(self.parse_query_string(part))

    # Make a node for the current token
    node = self.operators[token](children)
    return node