def ShouldCheckNamespaceIndentation(nesting_state, is_namespace_indent_item,
                                    raw_lines_no_comments, linenum):
  """This method determines if we should apply our namespace indentation check.

  Args:
    nesting_state: The current nesting state.
    is_namespace_indent_item: If we just put a new class on the stack, True.
      If the top of the stack is not a class, or we did not recently
      add the class, False.
    raw_lines_no_comments: The lines without the comments.
    linenum: The current line number we are processing.

  Returns:
    True if we should apply our namespace indentation check. Currently, it
    only works for classes and namespaces inside of a namespace.
  """

  is_forward_declaration = IsForwardClassDeclaration(raw_lines_no_comments,
                                                     linenum)

  if not (is_namespace_indent_item or is_forward_declaration):
    return False

  # If we are in a macro, we do not want to check the namespace indentation.
  if IsMacroDefinition(raw_lines_no_comments, linenum):
    return False

  return IsBlockInNameSpace(nesting_state, is_forward_declaration)