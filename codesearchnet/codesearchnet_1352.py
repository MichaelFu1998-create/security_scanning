def importAndRunFunction(
    path,
    moduleName,
    funcName,
    **keywords
  ):
  """
  Run a named function specified by a filesystem path, module name
  and function name.

  Returns the value returned by the imported function.

  Use this when access is needed to code that has
  not been added to a package accessible from the ordinary Python
  path. Encapsulates the multiple lines usually needed to
  safely manipulate and restore the Python path.

  Parameters
  ----------
  path: filesystem path
  Path to the directory where the desired module is stored.
  This will be used to temporarily augment the Python path.

  moduleName: basestring
  Name of the module, without trailing extension, where the desired
  function is stored. This module should be in the directory specified
  with path.

  funcName: basestring
  Name of the function to import and call.

  keywords:
  Keyword arguments to be passed to the imported function.
  """
  import sys
  originalPath = sys.path
  try:
    augmentedPath = [path] + sys.path
    sys.path = augmentedPath
    func = getattr(__import__(moduleName, fromlist=[funcName]), funcName)
    sys.path = originalPath
  except:
    # Restore the original path in case of an exception.
    sys.path = originalPath
    raise
  return func(**keywords)