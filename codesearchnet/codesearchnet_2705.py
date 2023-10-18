def get_sub_parts(self, query):
    """The subparts are seperated by a comma. Make sure
    that commas inside the part themselves are not considered."""
    parts = []
    num_open_braces = 0
    delimiter = ','
    last_starting_index = 0
    for i in range(len(query)):
      if query[i] == '(':
        num_open_braces += 1
      elif query[i] == ')':
        num_open_braces -= 1
      elif query[i] == delimiter and num_open_braces == 0:
        parts.append(query[last_starting_index: i].strip())
        last_starting_index = i + 1
    parts.append(query[last_starting_index:].strip())
    return parts