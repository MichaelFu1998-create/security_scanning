def _load_class(cls, d):
  """
  Loads additional properties into class `cls`.
  """
  for k, v in d.items():
    if isinstance(k, tuple):
      typ, k = k
      if typ == 'property':
        v = property(*v)
      elif typ == 'staticmethod':
        v = staticmethod(v) # pylint: disable=redefined-variable-type
      elif typ == 'classmethod':
        v = classmethod(v)
    setattr(cls, k, v)
  return cls