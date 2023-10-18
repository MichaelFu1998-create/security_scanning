def getCallerInfo(depth=2):
  """Utility function to get information about function callers

  The information is the tuple (function/method name, filename, class)
  The class will be None if the caller is just a function and not an object
  method.

  :param depth: (int) how far back in the callstack to go to extract the caller
         info

  """
  f = sys._getframe(depth)
  method_name = f.f_code.co_name
  filename = f.f_code.co_filename

  arg_class = None
  args = inspect.getargvalues(f)
  if len(args[0]) > 0:
    arg_name = args[0][0] # potentially the 'self' arg if its a method
    arg_class = args[3][arg_name].__class__.__name__
  return (method_name, filename, arg_class)