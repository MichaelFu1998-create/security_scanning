def hook(name):
  '''
  Decorator used to tag a method that should be used as a hook for the
  specified `name` hook type.
  '''
  def hookTarget(wrapped):
    if not hasattr(wrapped, '__hook__'):
      wrapped.__hook__ = [name]
    else:
      wrapped.__hook__.append(name)
    return wrapped
  return hookTarget