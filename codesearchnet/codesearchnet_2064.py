def parse_future_features(mod):
  """Accumulates a set of flags for the compiler __future__ imports."""
  assert isinstance(mod, ast.Module)
  found_docstring = False
  for node in mod.body:
    if isinstance(node, ast.ImportFrom):
      if node.module == '__future__':
        return node, _make_future_features(node)
      break
    elif isinstance(node, ast.Expr) and not found_docstring:
      if not isinstance(node.value, ast.Str):
        break
      found_docstring = True
    else:
      break
  return None, FutureFeatures()