def _fill_function(func, globalsn, defaults, dictn, module):
  """ Fills in the rest of function data into the skeleton function object
    that were created via _make_skel_func().
     """
  func.__globals__.update(globalsn)
  func.__defaults__ = defaults
  func.__dict__ = dictn
  func.__module__ = module

  return func