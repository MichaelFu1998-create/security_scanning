def IsBlockInNameSpace(nesting_state, is_forward_declaration):
  """Checks that the new block is directly in a namespace.

  Args:
    nesting_state: The _NestingState object that contains info about our state.
    is_forward_declaration: If the class is a forward declared class.
  Returns:
    Whether or not the new block is directly in a namespace.
  """
  if is_forward_declaration:
    return len(nesting_state.stack) >= 1 and (
      isinstance(nesting_state.stack[-1], _NamespaceInfo))


  return (len(nesting_state.stack) > 1 and
          nesting_state.stack[-1].check_namespace_indentation and
          isinstance(nesting_state.stack[-2], _NamespaceInfo))