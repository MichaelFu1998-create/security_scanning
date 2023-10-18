def _make_future_features(node):
  """Processes a future import statement, returning set of flags it defines."""
  assert isinstance(node, ast.ImportFrom)
  assert node.module == '__future__'
  features = FutureFeatures()
  for alias in node.names:
    name = alias.name
    if name in _FUTURE_FEATURES:
      if name not in _IMPLEMENTED_FUTURE_FEATURES:
        msg = 'future feature {} not yet implemented by grumpy'.format(name)
        raise util.ParseError(node, msg)
      setattr(features, name, True)
    elif name == 'braces':
      raise util.ParseError(node, 'not a chance')
    elif name not in _REDUNDANT_FUTURE_FEATURES:
      msg = 'future feature {} is not defined'.format(name)
      raise util.ParseError(node, msg)
  return features