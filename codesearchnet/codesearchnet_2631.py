def valid_path(path):
  '''
  Check if an entry in the class path exists as either a directory or a file
  '''
  # check if the suffic of classpath suffix exists as directory
  if path.endswith('*'):
    Log.debug('Checking classpath entry suffix as directory: %s', path[:-1])
    if os.path.isdir(path[:-1]):
      return True
    return False

  # check if the classpath entry is a directory
  Log.debug('Checking classpath entry as directory: %s', path)
  if os.path.isdir(path):
    return True
  else:
    # check if the classpath entry is a file
    Log.debug('Checking classpath entry as file: %s', path)
    if os.path.isfile(path):
      return True

  return False