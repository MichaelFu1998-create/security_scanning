def _allow_new_attributes(f):
  """A decorator that maintains the attribute lock state of an object

  It coperates with the LockAttributesMetaclass (see bellow) that replaces
  the __setattr__ method with a custom one that checks the _canAddAttributes
  counter and allows setting new attributes only if _canAddAttributes > 0.

  New attributes can be set only from methods decorated
  with this decorator (should be only __init__ and __setstate__ normally)

  The decorator is reentrant (e.g. if from inside a decorated function another
  decorated function is invoked). Before invoking the target function it
  increments the counter (or sets it to 1). After invoking the target function
  it decrements the counter and if it's 0 it removed the counter.
  """
  def decorated(self, *args, **kw):
    """The decorated function that replaces __init__() or __setstate__()

    """
    # Run the original function
    if not hasattr(self, '_canAddAttributes'):
      self.__dict__['_canAddAttributes'] = 1
    else:
      self._canAddAttributes += 1
    assert self._canAddAttributes >= 1

    # Save add attribute counter
    count = self._canAddAttributes
    f(self, *args, **kw)

    # Restore _CanAddAttributes if deleted from dict (can happen in __setstte__)
    if hasattr(self, '_canAddAttributes'):
      self._canAddAttributes -= 1
    else:
      self._canAddAttributes = count - 1

    assert self._canAddAttributes >= 0
    if self._canAddAttributes == 0:
      del self._canAddAttributes

  decorated.__doc__ = f.__doc__
  decorated.__name__ = f.__name__
  return decorated