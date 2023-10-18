def _make_skel_func(code, closures, base_globals=None):
  """ Creates a skeleton function object that contains just the provided
    code and the correct number of cells in func_closure.  All other
    func attributes (e.g. func_globals) are empty.
  """
  closure = _reconstruct_closure(closures) if closures else None

  if base_globals is None:
    base_globals = {}
  base_globals['__builtins__'] = __builtins__

  return types.FunctionType(code, base_globals, None, None, closure)