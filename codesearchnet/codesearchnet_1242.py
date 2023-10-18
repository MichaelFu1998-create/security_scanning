def _simple_init(self, *args, **kw):
  """trivial init method that just calls base class's __init__()

  This method is attached to classes that don't define __init__(). It is needed
  because LockAttributesMetaclass must decorate the __init__() method of
  its target class.
  """
  type(self).__base__.__init__(self, *args, **kw)